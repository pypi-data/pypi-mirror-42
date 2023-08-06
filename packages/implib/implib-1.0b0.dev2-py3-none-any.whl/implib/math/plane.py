import numpy as np

__all__ = ['Plane']


class Plane:
	def __init__(self, origin, normal):
		self._origin, self._normal = None, None
		self.set_origin(origin)
		self.set_normal(normal)

	def set_origin(self, p):
		self._origin = p

	def set_normal(self, v):
		self._normal = v

	def get_origin(self):
		return self._origin

	def get_normal(self):
		return self._normal

	def contains_point(self, p, tol=None):
		"""
		"""
		return np.dot(self._normal, p - self._origin) == 0.

	def find_seg_intersection(self, p1, p2):
		"""Determine if a line segment intersects this plane.
		If so, calculate the pose at the intersection.

		Args:
			p1 (numpy-array): (6,) array representing one end-pose of the segment
			p2 (numpy-array): (6,) array representing the other end-pose of the segment

		Returns:
			numpy-array: (3,) array representing the point of intersection
			None: if there is no intersection or if line is coincident
		"""
		u = p2[:3] - p1[:3]

		# Check if line is parallel to the plane
		if np.dot(self._normal, u) == 0.:
			return None  # line is either coincident or there is no intersection

		s = np.dot(self._normal, self._origin - p1[:3]) / np.dot(self._normal,
		                                                         u)

		if s >= 0 and s <= 1:
			return p1 + (s * (p2 - p1))
		else:
			return None


# TODO: add to Tests
def test_plane_find_seg_intersection():
	p1, p2 = np.array([1., 0., 1.]), np.array([4., -2., 2.])
	expected_p1 = np.array([7., -4., 3.])
	plane = Plane(np.array([2., 2., 2.]), np.array([1., 1., 1.]))
	assert plane.find_seg_intersection(p1, p2) is None

	plane = Plane(np.array([0., 0., 0., ]), np.array([0., 0., 1.]))
	p1, p2 = np.array([0., 0., -1.]), np.array([0., 0., 2.])
	assert np.array_equal(plane.find_seg_intersection(p1, p2),
	                      np.array([0., 0., 0.]))


if __name__ == '__main__':
	test_plane_find_seg_intersection()
