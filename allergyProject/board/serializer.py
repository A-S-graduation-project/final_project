from rest_framework import serializers
from .models import Board, BoardImage

class BoardImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = BoardImage
        fields = ['image', 'ex_image']

class BoardSerializer(serializers.ModelSerializer):
    images = BoardImageSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['title', 'content']

    def create(self, validate_data):
        instance = Board.objects.create(**validate_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            BoardImage.objects.create(board=instance, image=image_data)
        return instance