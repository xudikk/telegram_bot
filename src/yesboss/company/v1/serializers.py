from rest_framework import serializers
from ..models import Companies
from ...user.models import Users

class CompanySerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=255, required=False)
    title = serializers.CharField(max_length=200, required=False, )
    description = serializers.CharField(max_length=800, required=False)
    phone_number = serializers.CharField(max_length=20, required=True)
    address = serializers.CharField(max_length=500, required=False)

    user = serializers.IntegerField(required=True, )
    region = serializers.IntegerField(required=True, )
    district = serializers.IntegerField(required=True, )
    status = serializers.IntegerField(required=True, )

    def __init__(self, *args, **kwargs):
        self.company_id = kwargs.pop('company')
        super(CompanySerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        company_email = attrs.get('email', 0)
        user = attrs.get('user', 0)
        try:
            company_obj = Companies.objects.get(email=company_email)
            if self.company_id and company_obj and company_obj.id == self.company_id:
                company_obj = None
        except Companies.DoesNotExist:
            company_obj = None
        if company_obj:
            raise serializers.ValidationError({'email': ['Email already exists']})

        if user:
            try:
                self.user_obj = Users.objects.get(id=user)
            except Users.DoesNotExist:
                raise serializers.ValidationError({'user': ['User not found']})

        return attrs

    def save(self):

        if self.company_id:
            try:
                company_model = Companies.objects.get(id=self.company_id)
            except Companies.DoesNotExist:
                raise serializers.ValidationError({'company_id': ['company found region']})
        else:
            company_model = Companies()

        company_name = self.validated_data.get('company_name', company_model.company_name)
        email = self.validated_data.get('email', company_model.email)
        title = self.validated_data.get('title', company_model.title)
        description = self.validated_data.get('description', company_model.description)
        phone_number = self.validated_data.get('phone_number', company_model.phone_number)
        address = self.validated_data.get('address', company_model.address)
        if company_model and company_model.user:
            user = self.validated_data.get('user', company_model.user.id)
            status = self.validated_data.get('status', company_model.status.id)
            district = self.validated_data.get('district', company_model.district_id)
            region = self.validated_data.get('region', company_model.region_id)
        else:
            user = self.validated_data.get('user', None)
            status = self.validated_data.get('status', None)
            district = self.validated_data.get('district', None)
            region = self.validated_data.get('region', None)

        company_model.company_name = company_name
        company_model.email = email
        company_model.title = title
        company_model.description = description
        company_model.phone_number = phone_number
        company_model.address = address
        company_model.user_id = user
        company_model.status_id = status
        company_model.district_id = district
        company_model.region_id = region
        company_model.save()

        return company_model

