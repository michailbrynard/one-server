# Custom Views
# ---------------------------------------------------------------------------------------------------------------------#
class ListCities(generics.ListAPIView):
    """
    API endpoint that allows cities to be viewed.
    """
    queryset = City.objects.all()
    serializer_class = CityBasicSerializer

    # Set pagination
    paginate_by = 100
    paginate_by_param = 'page_size'
    # Set MAX results per page
    max_paginate_by = 24000


class ListCategories(generics.ListAPIView):
    """
    API endpoint that allows categories to be viewed.
    """
    queryset = Category.objects.all()
    serializer_class = CategoryBasicSerializer

    # Set pagination
    paginate_by = 50
    paginate_by_param = 'page_size'
    # Set MAX results per page
    max_paginate_by = 50


# Custom User Views
# ---------------------------------------------------------------------------------------------------------------------#
class ListCreateQuestion(generics.ListCreateAPIView):
    """
    API endpoint that list the user's questions, and allows an user to create a question.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token"
    http://localhost:9090/api/asker/questions/

    curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT token"
    -d '{"question":"Testing the tool.", "city":"2", "category":"2"}'
    http://localhost:9090/api/asker/questions/
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return CreateQuestionSerializer
        return ListQuestionSerializer

    def get_queryset(self):
        """
        This view should return a list of all the questions
        for the currently authenticated user.
        """
        return Question.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": "success", "results": serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)


class ChannelQuestion(generics.ListAPIView):
    """
    API endpoint that lists all the first answers from experts for each question.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token"
    http://localhost:9090/api/asker/channels/1/
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = ListChannelSerializer

    lookup_url_kwarg = "question"

    def get_queryset(self):
        """
        This view should return a list of all the questions
        for the currently authenticated user.
        """
        question = self.kwargs.get(self.lookup_url_kwarg)
        return Channel.objects.filter(user=self.request.user, question=question)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint that allows authenticated user profile to be viewed or updated.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token" http://localhost:9090/api/profile/

    curl -X PUT -H "Content-Type: application/json" -H "Authorization: JWT token"
    -d '{"user":{"first_name":"Test500", "last_name":"Tester500", "birthday":"1989-12-19", "gender":"Male",
    "bio":"I am superman."}, "promo_code":"500", "home_city":2, "current_city":2, "nationality":2,
    "status":"Active"}' http://localhost:9090/api/profile/
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'PUT':
            return UpdateProfileSerializer
        return ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        return obj

    def put(self, request, *args, **kwargs):
        """
        Both UpdateProfileSerializer and UserBasicSerializer are required
        in order to validate and save data on their associated models.
        """

        data = request.data
        # username = request.data.pop('username')
        profile_instance = UserBasic.objects.get(id=request.user.id).profile
        update_profile_serializer = UpdateProfileSerializer(instance=profile_instance,
                                                            data=data, partial=True)
        if update_profile_serializer.is_valid():
            update_profile_serializer.save()
            get_profile = ProfileSerializer(instance=profile_instance)
            return Response(get_profile.data, status=status.HTTP_200_OK)
        else:
            # Combine errors from both serializers.
            errors = dict()
            errors.update(update_profile_serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# Custom Expert Views
# ---------------------------------------------------------------------------------------------------------------------#
class ListQuestionExpert(generics.ListAPIView):
    """
    API endpoint that provides all the questions available for
    experts to answer.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token"
    http://localhost:9090/api/expert/questions/
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = ListQuestionExpertSerializer

    def get_queryset(self):
        """
        This view should return a list of all the questions
        for the currently authenticated user.
        """
        return Question.objects.filter(status='Pending')


class ChannelQuestionExpert(generics.ListCreateAPIView):
    """
    API endpoint that provides information of a single question.
    Expert can submit a response by doing a POST request. The initial
    POST creates a channel.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token"
    http://localhost:9090/api/expert/question/1/

    curl -X POST -H "Content-Type: application/json" -H "Authorization: JWT token"
    -d '{"message":"First response.", "uni_channel_id":"123456789"}'
    http://localhost:9090/api/expert/questions/1/
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    lookup_url_kwarg = "question"

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return CreateChannelExpertSerializer
        return ListQuestionExpertSerializer

    def get_queryset(self):
        """
        This view should return a list of all the questions
        for the currently authenticated user.
        """
        question = self.kwargs.get(self.lookup_url_kwarg)
        return Question.objects.filter(id=question)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        question = self.kwargs.get(self.lookup_url_kwarg)
        if not Channel.objects.filter(question_id=question, expert_id=request.user.id).exists():
            question_obj = Question.objects.get(id=question)
            data = {'question': question_obj.id,
                    'expert': request.user.id,
                    'user': question_obj.user.id,
                    'message': request.data['message'],
                    'uni_channel_id': request.data['uni_channel_id']
                }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"status": "success", "results":serializer.data},
                            status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"status": "error", "message": "Only one channel response allowed. Redirect user to chat."},
                            status=status.HTTP_403_FORBIDDEN)


class ListChannelExpert(generics.ListAPIView):
    """
    API endpoint that provides all the questions answered by the expert.

    curl -X GET -H "Content-Type: application/json" -H "Authorization: JWT token"
    http://localhost:9090/api/expert/channels/
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    serializer_class = ListChannelExpertSerializer

    def get_queryset(self):
        """
        This view should return a list of all the questions
        for the currently authenticated user.
        """
        return Channel.objects.filter(expert=self.request.user)