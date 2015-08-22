# Custom Serializers for User
# ---------------------------------------------------------------------------------------------------------------------#
class ListQuestionSerializer(serializers.ModelSerializer):

    city = serializers.SerializerMethodField(source='get_city')
    category = serializers.SerializerMethodField(source='get_category')
    channel_count = serializers.SerializerMethodField(source='get_channel_count')

    class Meta:
        model = Question
        fields = ('id', 'city', 'category', 'question', 'status',
                  'created_timestamp', 'updated_timestamp', 'channel_count')

    def get_city(self, obj):
        try:
            return obj.city.name
        except:
            return None

    def get_category(self, obj):
        try:
            return obj.category.description
        except:
            return None

    def get_channel_count(self, obj):
        counter = Channel.objects.filter(question=obj.id).count()
        return counter


class CreateQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('city', 'category', 'question', 'created_timestamp')


class ListChannelSerializer(serializers.ModelSerializer):

    question = ListQuestionSerializer()
    expert_info = serializers.SerializerMethodField(source='get_expert_info')
    chat_count = serializers.SerializerMethodField(source='get_chat_count')

    class Meta:
        model = Channel
        fields = ('user', 'question', 'expert_info', 'status', 'message', 'chat_count',
                  'uni_channel_id', 'activation_timestamp', 'created_timestamp', 'updated_timestamp')

    def get_expert_info(self, obj):
        profile_obj = Profile.objects.get(user_id=obj.expert.id)
        serialized_obj = ProfileHyperSerializer(profile_obj, context=self.context)
        return serialized_obj.data

    def get_chat_count(self, obj):
        counter = Chat.objects.filter(channel=obj.id).count()
        return counter


class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField(source='get_user')
    home_city = serializers.SerializerMethodField(source='get_home_city')
    current_city = serializers.SerializerMethodField(source='get_current_city')
    nationality = serializers.SerializerMethodField(source='get_nationality')

    class Meta:
        model = Profile
        fields = ('user', 'home_city', 'current_city', 'nationality', 'profile_picture',
                  'promo_code', 'status')

    def get_user(self, obj):
        user_obj = UserBasic.objects.get(id=obj.user_id)
        serialized_obj = UserHyperSerializer(user_obj, context=self.context)
        return serialized_obj.data

    def get_home_city(self, obj):
        try:
            return obj.home_city.name
        except:
            return None

    def get_current_city(self, obj):
        try:
            return obj.current_city.name
        except:
            return None

    def get_nationality(self, obj):
        try:
            return obj.nationality.name
        except:
            return None


class UpdateProfileSerializer(serializers.ModelSerializer):

    user = UpdateUserSerializer()

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        user_instance = instance.user
        for attr, value in user.items():
            if not ((attr == 'username') and (user_instance.username == value)):
                setattr(user_instance, attr, value)

        user_instance.save()

        return instance

    class Meta:
        model = Profile
        fields = ('user', 'profile_picture', 'promo_code', 'home_city', 'current_city', 'nationality', 'status')


# Custom Serializers for Expert
# ---------------------------------------------------------------------------------------------------------------------#
class ListQuestionExpertSerializer(serializers.ModelSerializer):

    user_info = serializers.SerializerMethodField(source='get_user_info')
    city = serializers.SerializerMethodField(source='get_city')
    category = serializers.SerializerMethodField(source='get_category')
    channel_count = serializers.SerializerMethodField(source='get_channel_count')
    channel_info = serializers.SerializerMethodField(source='get_channel_info')

    class Meta:
        model = Question
        fields = ('id', 'user_info', 'city', 'category', 'question', 'status',
                  'created_timestamp', 'updated_timestamp', 'channel_count',
                  'channel_info')

    def get_user_info(self, obj):
        profile_obj = Profile.objects.get(user_id=obj.user.id)
        serialized_obj = ProfileHyperSerializer(profile_obj, context=self.context)
        return serialized_obj.data

    def get_city(self, obj):
        try:
            return obj.city.name
        except:
            return None

    def get_category(self, obj):
        try:
            return obj.category.description
        except:
            return None

    def get_channel_count(self, obj):
        counter = Channel.objects.filter(question=obj.id).count()
        return counter

    def get_channel_info(self, obj):
        try:
            channel_obj = Channel.objects.get(question_id=obj.id, expert=self.context['request'].user)
            serialized_obj = SubChannelExpertSerializer(channel_obj, context=self.context)
            return serialized_obj.data
        except ObjectDoesNotExist:
            return None


class SubChannelExpertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ('message', 'uni_channel_id')

    def get_expert_info(self, obj):
        profile_obj = Profile.objects.get(user_id=obj.expert.id)
        serialized_obj = ProfileHyperSerializer(profile_obj, context=self.context)
        return serialized_obj.data


class ListChannelExpertSerializer(serializers.ModelSerializer):

    expert_info = serializers.SerializerMethodField(source='get_expert_info')
    user_info = serializers.SerializerMethodField(source='get_user_info')

    class Meta:
        model = Channel
        fields = ('question', 'expert_info', 'user_info', 'message')

    def get_user_info(self, obj):
        profile_obj = Profile.objects.get(user_id=obj.user.id)
        serialized_obj = ProfileHyperSerializer(profile_obj, context=self.context)
        return serialized_obj.data

    def get_expert_info(self, obj):
        profile_obj = Profile.objects.get(user_id=obj.expert.id)
        serialized_obj = ProfileHyperSerializer(profile_obj, context=self.context)
        return serialized_obj.data


class CreateChannelExpertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ('question', 'expert', 'user', 'message', 'uni_channel_id')