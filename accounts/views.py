# from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
# from rest_framework.permissions import IsAuthenticated
# from .models import UserAccount
# from .permissions import IsOwnerProfileOrReadOnly
# from .serializers import UserCreateSerializer

# # Create your views here.

# class UserProfileListCreateView(ListCreateAPIView):
#     queryset=UserAccount.objects.all()
#     serializer_class=UserCreateSerializer
#     permission_classes=[IsAuthenticated]

#     def perform_create(self, serializer):
#         user=self.request.user
#         serializer.save(user=user)


# class userProfileDetailView(RetrieveUpdateDestroyAPIView):
#     queryset=UserAccount.objects.all()
#     serializer_class=UserCreateSerializer
#     permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]