from django.contrib.auth.models import User

#from checkers.models import UserProfile

class AuthenticationBackendAnonymous:
	'''
		This is for automatically signing in the user after signup etc.
	'''
	def authenticate(self, user=None):
		# make sure they have a profile and that they are anonymous
		# if you're not using profiles you can just return user
		if not user.get_profile() or not user.get_profile().anonymous:
			user = None
		return user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
