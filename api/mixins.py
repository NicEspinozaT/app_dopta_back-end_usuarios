from firebasestorage.firebase import bucket


class FirebaseImageMixin:
    def upload_image_to_firebase(self, instance, imagen_perfil):
        blob = bucket.blob(
            f"imagen_perfil/{instance.user.username}.{imagen_perfil.name.split('.')[-1]}"
        )
        blob.upload_from_file(
            imagen_perfil.file, content_type=imagen_perfil.content_type
        )
        blob.make_public()

        public_url = blob.public_url

        instance.imagen_perfil = public_url
        instance.save()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["imagen_perfil"] = (
            instance.imagen_perfil if instance.imagen_perfil else None
        )
        return representation
