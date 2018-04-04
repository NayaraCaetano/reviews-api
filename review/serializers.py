from rest_framework import serializers

from review.models import Review, Company


class ReviewCompanySerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField()

    class Meta:
        model = Company
        fields = ('name', 'company_id', 'website')


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    company = ReviewCompanySerializer()

    class Meta:
        model = Review
        fields = (
            'rating', 'title', 'summary', 'ip_address', 'submission_date',
            'company', 'reviewer'
        )
        read_only_fields = ('ip_address', 'reviewer', 'submission_date')

    def create(self, validated_data):
        company_data = validated_data.pop('company')
        company, _ = Company.objects.update_or_create(
            company_id=company_data.pop('company_id'),
            defaults=company_data
        )
        review = Review.objects.create(company=company, **validated_data)
        return review
