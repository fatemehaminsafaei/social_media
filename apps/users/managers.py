# from django.db import models
#
# from apps.users.models.users import Profile
#
#
# # class RelationshipManager(models.Manager):
# #
# #     def invitation_received(self, receiver):
# #         qs = Relationship.objects.filter(receiver=receiver, status='send')
# #         return qs
#
#
#
#
#
# class ProfileManager(models.Manager):
#
#     def get_profiles(self, sender):
#         profiles = Profile.objects.all().exclude(user=sender)
#         profile = Profile.objects.get(user=sender)
#         qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
#
#         accepted = set([])
#         for rel in qs:
#             if rel.status == 'accepted':
#                 # because are either receiver or sender using set prevents repetition in list
#                 accepted.add(rel.receiver)
#                 accepted.add(rel.sender)
#
#         available = [profile for profile in profiles if profile not in accepted]  # all the available profile to invite
#         print(available)
#         return available
#
#     def get_all_profiles(self, me):#
#         profiles = Profile.objects.all().exclude(user=me)
#         return profiles