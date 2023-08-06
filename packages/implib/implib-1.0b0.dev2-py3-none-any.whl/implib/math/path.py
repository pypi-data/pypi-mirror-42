import numpy as np
import csv
import os.path
import glob
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
# print(plotly.__version__)

from implib.math.plane import Plane
import implib.fileutils as futils
from implib.cutfile import CutFile


class Path:

	# TODO: Update length attribute on loading

	EXTENSION = r'.path'

	def __init__(self, pose_array=None, name=None):
		"""Path constructor.

		Args:
			pose_array (numpy.array):
			name (string):
		"""
		self.name = name
		self._path = None
		self.length = 0
		self._trace_color = None

		if pose_array is not None:
			self.set_path(pose_array)

	def set_name(self, name):
		"""Set the name of this Path.

		Args:
			name (string): the new desired name.	
		"""
		self.name = name

	def set_trace_color(self, r, g, b, a=1.0):
		self._trace_color = 'rgba(%s,%s,%s,%s)' % (r, g, b, a)

	def set_path(self, pose_array):
		"""Set the path to a new path. 

		Args:
			pose_array (numpy.array):
		"""
		if pose_array.shape[1] != 6:
			raise RuntimeError('pose_array must be have shape (n, 6).')
		self._path = pose_array
		self.length = self._path.shape[0]

	def append(self, pose):
		return NotImplemented

	def get_path(self, axis=None):
		"""Retrieve the current path.

		Args:
			axis (string): can be 'x', 'y', 'z', 'a', 'b', or 'c'. Default is None, which returns all axes.

		Returns:
			(numpy.array)
		"""
		if isinstance(axis, str):
			axis = axis.lower()

		if axis == 'x':
			return self._path[:, 0]
		elif axis == 'y':
			return self._path[:, 1]
		elif axis == 'z':
			return self._path[:, 2]
		elif axis == 'a':
			return self._path[:, 3]
		elif axis == 'b':
			return self._path[:, 4]
		elif axis == 'c':
			return self._path[:, 5]
		else:
			return self._path

	def load(self, file_path):
		temp_path_obj = load_path(file_path)
		self.name = temp_path_obj.name
		self._trace_color = temp_path_obj._trace_color
		self.set_path(temp_path_obj.get_path())

	def transform(self, tfm):
		"""
		Apply a 4x4 Homogenous Transform to all poses in the path.

		Args:
			tfm (numpy-array): 4x4 homogenous transformation matrix

		Raises:
			RuntimeError: if tfm does not have shape == (4,4)

		Notes:
			- Updates Path._path
		"""
		if tfm.shape != (4, 4):
			raise RuntimeError(
				'tfm must have shape (4,4). tfm has shape %s instead.' % tfm.shape)

		pts = np.vstack((self._path[:, :3].T, np.ones(self._path.shape[0])))
		vecs = np.vstack((self._path[:, 3:].T, np.zeros(self._path.shape[0])))
		pts = np.dot(tfm, pts)[:3].T
		vecs = np.dot(tfm, vecs)[:3].T
		self._path = np.hstack((pts, vecs))
		return self

	def plotly_trace(self):
		# TODO: Make this work with **kwargs
		return go.Scatter3d(
			x=self.get_path(axis='x'),
			y=self.get_path(axis='y'),
			z=self.get_path(axis='z'),
			mode='lines+markers+text',
			name=self.name,
			line=dict(width=1, color=self._trace_color),
			marker=dict(size=2, color=self._trace_color),
			opacity=1.0,
			hovertext=['Sample Index: %s' % i for i in range(1, self.length + 1)],
			hoverlabel=dict(font=dict(size=8))
		)

	def normal_planes(self):
		norms = []
		for i in range(self._path.shape[0] - 1):
			if np.allclose(self._path[i][:3], self._path[i+1][:3], rtol=0., atol=1e-8):
				norms.append(None)
				continue
			normal = (self._path[i+1] - self._path[i])[:3]
			normal = normal / np.linalg.norm(normal)
			origin = self._path[i][:3]
			norms.append(Plane(origin, normal))
		return np.array(norms)

	def get_segs(self, connect_ends=False):
		"""Returns entire pose (location and orientation)"""
		segs = [[self._path[i], self._path[i+1]] for i in range(self._path.shape[0]-1)]
		if connect_ends:
			segs.append([self._path[-1], self._path[0]])
		return np.array(segs)

	def find_plane_intersection(self, plane, connect_ends=False):
		"""
		Notes:
			- If there are multiple intersections, return the intersection (pose) closest to the plane origin.
		"""
		closest_int, min_dist = None, float('inf')
		# eventually remove call to get_segs() for optimize
		for seg in self.get_segs(connect_ends=connect_ends):
			intersection = plane.find_seg_intersection(seg[0], seg[1])
			if intersection is not None:
				dist = np.linalg.norm(intersection[:3] - plane.get_origin())
				if closest_int is None or dist < min_dist:
					closest_int = intersection
					min_dist = dist
		return closest_int

	def add_noise(self, pos_mean=0.0, pos_sigma=1.0, ori_mean=0.0, ori_sigma=1.0):
		for i, pose in enumerate(self._path):
			self._path[i, :3] += np.random.normal(pos_mean, pos_sigma, 3)
			self._path[i, 3:] += np.random.normal(ori_mean, ori_sigma, 3)

	def save(self, save_dir, name=None):
		if futils.is_dir(save_dir):
			if name is None:
				if self.name is None:
					raise RuntimeError('Must provide file name or set name of the Path object!')
				else:
					name = self.name
			full_fname = futils.make_file_name(save_dir, name, self.EXTENSION)
			futils.save_pickle(self, full_fname, 0)
			return full_fname


def load_path(file_path, name=None):
	name = file_path if name is None else name

	if futils.is_cut_file(file_path):
		cut = CutFile()
		cut.read(file_path)
		pose_list = cut.get_pose_list2()
	elif futils.check_ext(file_path, 'csv'):
		pose_list = read_pose_array_from_tracker_sequence(file_path)
	elif futils.check_ext(file_path, 'txt'):
		pose_list = read_pose_array_from_log(file_path)
	elif futils.check_ext(file_path, Path.EXTENSION):
		path = futils.load_pickle(file_path)
		path.set_name(name)
		return path
	else:
		raise FileNotFoundError('File %s is not a valid Path file-type '
		                        'because extension \'%s\' is not supported!'
		                        % (file_path, futils.get_ext(file_path)))

	return Path(pose_array=pose_list, name=name)


def read_pose_array_from_tracker_sequence(tracker_seq_file_path):
	"""Read a Tracker Sequence (csv) file

	Args: string - file path to tracker seq

	Return pose array object
	"""
	# TODO: add fname to check if row was valid
	fnames = ['TX', 'TY', 'TZ', 'RX', 'RY', 'RZ']
	poses = []
	with open(tracker_seq_file_path, 'r') as track_seq:
		reader = csv.DictReader(track_seq, fieldnames=fnames)
		next(reader)
		next(reader)
		for row in reader:
			poses.append([float(row['TX']),
			              float(row['TY']),
			              float(row['TZ']),
			              float(row['RX']),
			              float(row['RY']),
			              float(row['RZ'])])
	return np.array(poses)


def read_path_from_tracker_sequence(tracker_seq_file_path):
	"""Read a Tracker Sequence (csv) file

	Args: string - file path to tracker seq

	Return implib.math.path.Path object
	"""
	return Path(read_pose_array_from_tracker_sequence(tracker_seq_file_path))


def read_pose_array_from_log(log_file_path):
	"""Extract commanded path from TCAT log file.

	Args: string - file path to log file

	Returns pose array
	"""
	poses = []
	log_path_token = r'INFO(CsMotionLogServer.cpp:onMsgReceive'

	with open(log_file_path, 'r') as logfile:
		for line in logfile:
			idx = line.find(log_path_token)
			if idx >= 0:
				chunks = line.split()
				x, y, z, r, p = list(
					map(lambda x: float(x.split('=')[1]), chunks[-8:-3]))
				# TODO: resolve Roll and Pitch
				poses.append([x, y, z, None, None, None])
	return np.array(poses)


def read_path_from_log(log_file_path):
	"""Extract commanded path from TCAT log file.

	Args: string - file path to log file

	Returns implib.math.path.Path object
	"""
	return Path(read_pose_array_from_log(log_file_path))


def read_path_dir(dir_path):
	"""
	For a directory of csv files, where each file contains a tracked-model path, convert each path 
	into a numpy array of poses.

	Args:
		dir_path (string): path to the directory containing the csv files

	Returns:
		dictionary: key - file name, value - numpy-array of poses.

	Notes:
		- The csv files must have unique column names "TX", "TY", "TZ", "RX", "RY", and "RZ",
		(blank column names are allowed, but those 6 must exist). Order does not matter. 
		These column names must be the first row of the file, i.e. the header.
	"""
	if os.path.isdir(dir_path):
		dir_path = os.path.abspath(dir_path)
		paths = []
		for fname in glob.glob(dir_path + '\*.csv'):
			path = Path(file_path=fname, name=os.path.basename(fname))
			paths.append(path)
		return paths
	else:
		return None


def test_read_path_dir():
	test_paths = read_path_dir(
		r'X:\Individual Folders\CJG\Burn-in Testing\data\tracker_data_group_example')
	print(test_paths)


def create_3x_xy_square_path(side_len, seg_len, a=0., b=0., c=1., ccw=True,
                             name='3x__xy_square'):
	"""
	Create a segmented path for a 3-axis square cut-path in the XY-plane.

	Args:
		side_len (float): side length of square in mm  
		seg_len (float): path segment length in mm
		a (float): x orientation for duration of path. Default is 0.
		b (float): y orientation for duration of path. Default is 0.
		c (float): z orientation for duration of path. Default is 1.
		ccw (bool): direction of path (counter-clockwise). Default is True.

	Returns:
		numpy-array: each row is a pose -- (x, y, z, a, b, c) -- along the path.

	Notes:
		- The path will always start and end at the origin (0, 0, 0, a, b, c).
		- The path is entirely in the XY-plane, i.e. z = 0 for all poses.
	"""
	# round down to ensure that the segments aren't too short (minimum segment length for TCAT is 0.5 mm)
	num_segs = int(side_len / seg_len)
	seg_points = np.linspace(0., side_len, num_segs + 1, dtype=np.float64)
	zeros = np.zeros(num_segs)

	x = np.hstack((seg_points, side_len + zeros, seg_points[::-1][1:], zeros))
	y = x[::-1]
	num_points = len(x)
	z = np.zeros(num_points)
	a, b, c = a + np.zeros(num_points), b + np.zeros(num_points), c + np.zeros(
		num_points)

	pose_array = np.vstack((x, y, z, a, b, c)).T
	return Path(pose_array=pose_array, name=name)


def create_3x_xy_circle_path(rad, seg_len, a=0., b=0., c=1., ccw=True, std=None,
                             name='3x_xy_circle'):
	"""
	Create a segmented path for a 3-axis circular cut-path in the XY-plane.

	Args:
		rad (float): length of segment in mm  
		seg_len (float): path segment length in mm
		a (float): x orientation for duration of path. Default is 0.
		b (float): y orientation for duration of path. Default is 0.
		c (float): z orientation for duration of path. Default is 1.
		ccw (bool): direction of path (counter-clockwise). Default is True.

	Returns:
		Path object: each row is a pose -- (x, y, z, a, b, c) -- along the path.

	Notes:
		- The path will always start and end at the origin (0, 0, 0, a, b, c).
		- The path is entirely in the XY-plane, i.e. z = 0 for all poses.
	"""

	theta = 2 * np.arcsin(seg_len / (2 * rad))
	# round down to ensure that the segments aren't too short (minimum segment length for TCAT is 0.5 mm)
	num_points = int(2. * np.pi / theta) + 1
	seg_angles = 2 * np.pi * np.linspace(0, 1, num_points)

	if std is None:
		xs, ys = rad * np.cos(seg_angles), rad * np.sin(seg_angles)
	else:
		rads = np.random.normal(rad, std, num_points)
		xs, ys = [], []
		for i, r in enumerate(rads):
			xs.append(r * np.cos(seg_angles[i]))
			ys.append(r * np.sin(seg_angles[i]))

	zs = np.zeros(num_points)
	a, b, c = a + zs, b + zs, c + zs

	pose_array = np.vstack((xs, ys, zs, a, b, c)).T
	return Path(pose_array=pose_array, name=name)


def view_paths(*args, **kwargs):
	# TODO: add docstring
	# Create list of path traces
	trace_list = [path.plotly_trace() for path in args]

	# Create plot layout
	layout = go.Layout(
		title='Path Plot',
		scene=dict(
			aspectmode='data',
			aspectratio=dict(x=1, y=1, z=1),
			camera=dict(
				center=dict(x=0, y=0, z=0),
				eye=dict(x=3, y=3, z=3),
				up=dict(x=0, y=0, z=1)
			),
			dragmode='orbit',
		),
	)

	layout.update(kwargs)

	fig = go.Figure(data=trace_list, layout=layout)
	plot(fig)


def test_path_add_noise():
	circle_no_noise = create_3x_xy_circle_path(10., .5, name='No Noise')
	circle_no_noise.set_trace_color(0, 255, 0)
	circle_with_noise = create_3x_xy_circle_path(10., .5, name='With Noise')
	circle_with_noise.set_trace_color(255, 0, 0)
	circle_with_noise.add_noise(pos_sigma=.1, ori_sigma=.1)
	view_paths(circle_no_noise, circle_with_noise)


def some_tests_that_were_in_main():
	pose1 = np.array([0., 0., 0., 0., 0., 1.])
	pose2 = np.array([1., 0., 0., 0., 0., 1.])
	pose3 = np.array([2., 0., 0., 0., 0., 1.])
	pose4 = np.array([2., 1., 0., 0., 0., 1.])
	pose5 = np.array([2., 2., 0., 0., 0., 1.])
	pose6 = np.array([1., 2., 0., 0., 0., 1.])
	pose7 = np.array([0., 2., 0., 0., 0., 1.])
	pose8 = np.array([0., 1., 0., 0., 0., 1.])
	pose9 = np.array([0., 0., 0., 0., 0., 1.])

	sqaure_2x2 = np.array(
		[pose1, pose2, pose3, pose4, pose5, pose6, pose7, pose8, pose9])

	R_eye = np.eye(3)
	Ry_90 = np.array([[0., 0., 1.], [0., 1., 0.], [-1., 0., 0.]])
	Rz_90 = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 1.]])
	Rz_90_y_90 = np.dot(Ry_90, Rz_90)

	t0 = np.zeros((3, 1))
	t10 = t0 + 10
	fourth_row = np.array([0., 0., 0., 1.])

	tfm1 = np.vstack((np.hstack((R_eye, t0)), fourth_row))
	tfm2 = np.vstack((np.hstack((R_eye, t10)), fourth_row))
	tfm3 = np.vstack((np.hstack((Rz_90, t0)), fourth_row))
	tfm4 = np.vstack((np.hstack((Rz_90, t10)), fourth_row))
	tfm5 = np.vstack((np.hstack((Rz_90_y_90, t0)), fourth_row))

	path1 = Path(pose_array=sqaure_2x2, name='2x2 Square')
	path1.transform(tfm5)
	expected_path = np.array([[0, 0, 0, 1, 0, 0],
	                          [0, 1, 0, 1, 0, 0],
	                          [0, 2, 0, 1, 0, 0],
	                          [0, 2, 1, 1, 0, 0],
	                          [0, 2, 2, 1, 0, 0],
	                          [0, 1, 2, 1, 0, 0],
	                          [0, 0, 2, 1, 0, 0],
	                          [0, 0, 1, 1, 0, 0],
	                          [0, 0, 0, 1, 0, 0]
	                          ])
	assert np.array_equal(path1.get_path(),
	                      expected_path), 'Path.transform() not working!'
	fname1 = r'X:\Individual Folders\CJG\Burn-in Testing\data\xysquare50mm_test1_clean_long.csv'
	path2 = Path(file_path=fname1, name='from file')
	# print(path2.get_path().shape)

	test_read_path_dir()


def test_path_pickling():
	pose1 = np.array([0., 0., 0., 0., 0., 1.])
	pose2 = np.array([1., 0., 0., 0., 0., 1.])
	pose3 = np.array([2., 0., 0., 0., 0., 1.])
	pose4 = np.array([2., 1., 0., 0., 0., 1.])
	pose5 = np.array([2., 2., 0., 0., 0., 1.])
	pose6 = np.array([1., 2., 0., 0., 0., 1.])
	pose7 = np.array([0., 2., 0., 0., 0., 1.])
	pose8 = np.array([0., 1., 0., 0., 0., 1.])
	pose9 = np.array([0., 0., 0., 0., 0., 1.])

	square_2x2_path = np.array(
		[pose1, pose2, pose3, pose4, pose5, pose6, pose7, pose8, pose9])
	name = '2x2 Square'

	path_out = Path(square_2x2_path, name=name)
	save_dir = r'P:\Projects\ImpLibPythonPackage\tests\data'
	save_name = path_out.save(save_dir=save_dir)

	path_in = Path()
	path_in.load(save_name)
	print(path_in.get_path())

	path_in2 = load_path(save_name)
	print(path_in2.get_path(), path_in2.name)


def test_plotly_annotations():
	data2 = [go.Scatter3d(
		x=[0,1,2],
		y=[0,1,2],
		z=[0,1,2],
		mode='lines+markers+text',
		name='name',
		line=dict(width=2, color=None),
		marker=dict(size=2, color=None),
		opacity=0.9,
		hovertext=['Sample Index: %s' % i for i in range(1, len([0,1,2]) + 1)],
		hoverlabel=dict(font=dict(size=8))
	)]

	data = [go.Scatter3d(
		x=[0, 1, 2],
		y=[0, 1, 2],
		z=[0, 1, 2],
	)]

	layout = go.Layout(
		scene=dict(
			aspectmode='data',
			aspectratio=dict(
				x=1,
				y=1,
				z=1
			),
			camera=dict(
				center=dict(
					x=0,
					y=0,
					z=0
				),
				eye=dict(
					x=1.96903462608,
					y=-1.09022831971,
					z=0.405345349304
				),
				up=dict(
					x=0,
					y=0,
					z=1
				)
			),
			dragmode="turntable",
			annotations=[
				dict(
				x=20,
				y=20,
				z=20,
				ax=50,
				ay=0,
				text="Point 3",
				arrowhead=1,
				xanchor="left",
				yanchor="bottom"
			)]
		),
	)
	print(data)
	print(data2)
	fig = go.Figure(data=[data2[0],data2[0]], layout=layout)
	plot(fig)


if __name__ == '__main__':
	test_path_add_noise()
	# test_plotly_annotations()
	pass
