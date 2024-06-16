from firebasestorage.firebase import bucket
from PIL import Image
import io,os


class FirebaseImageMixin:
    def upload_image_to_firebase(self, instance, imagen_perfil):
        imagen = Image.open(imagen_perfil)
        jpg_image = io.BytesIO()
        imagen.convert("RGB").save(jpg_image, format="JPEG")
        jpg_image.seek(0)

        blob = bucket.blob(f"imagen_perfil/{instance.user.username}.jpg")
        blob.upload_from_file(jpg_image, content_type="image/jpeg")
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


class FirebaseDocMixin:
    def upload_document_to_firebase(self, instance, documento):

        username = instance.user.username
        doc_name, doc_extension = os.path.splitext(documento.name)
        
        # Nombre completo del archivo en Firebase Storage
        blob_name = f"doc_user/{username}/{username}{doc_extension}"
        
        # Subir el documento a Firebase Storage
        blob = bucket.blob(blob_name)
        blob.upload_from_file(documento)
        blob.make_public()  # Hacer el archivo público

        # Obtener la URL pública del documento
        public_url = blob.public_url

        # Guardar la URL en el modelo
        instance.documento = public_url
        instance.save()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["documento"] = instance.documento if instance.documento else None
        return representation
