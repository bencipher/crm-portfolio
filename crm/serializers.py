from rest_framework import serializers
from utilities.serializers_utils import ReadWriteSerializerMethodField
from users.serializers import CustomUserSerializer
from .models import *


class AgentSerializer(serializers.ModelSerializer):
    user = ReadWriteSerializerMethodField()

    class Meta:
        model = Agent
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        agent = Agent.objects.create(user=user)
        return agent

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_data.pop('password', None)
        CustomUser.objects.filter(id=instance.user.id).update(**user_data)
        instance.user = CustomUser.objects.get(id=instance.user.id)
        instance.save()
        return super().update(instance, validated_data)

    def get_user(self, obj):
        if obj.user:
            return CustomUserSerializer(obj.user).data
        return None


class LeadSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(write_only=True)
    assignee = ReadWriteSerializerMethodField(read_only=True)

    class Meta:
        model = Lead
        fields = '__all__'

    def get_assignee(self, obj):
        if obj.assignee:
            return AgentSerializer(obj.assignee).data
        return None

    def update(self, instance, validated_data):
        is_customer = False

        # ensure confirmed customers stage is not changed
        if instance.is_customer:
            assert validated_data['stage'] == 'Converted' and validated_data[
                'is_customer'] is True, ' Cannot change stage of already converted lead'

        # check if status is converted before updating to customer
        if validated_data.get('is_customer'):
            assert instance.stage == 'Converted' or validated_data[
                'stage'] == 'Converted', f"Lead of stage '{instance.stage}' cannot be converted  to Customer"

        instance.is_customer = is_customer
        instance.save()
        return super().update(instance, validated_data)
