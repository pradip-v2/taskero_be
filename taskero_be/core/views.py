from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from taskero_be.core.s3_utils import generate_presigned_upload_url
from taskero_be.core.serializers import GeneratePresignedURLRequestSerializer
from taskero_be.core.serializers import GeneratePresignedURLResponseSerializer
from taskero_be.core.serializers import ResponseSerializer


class GeneratePresignedURLView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=GeneratePresignedURLRequestSerializer,
        responses={
            200: GeneratePresignedURLResponseSerializer,
            400: ResponseSerializer,
        },
    )
    def post(self, request):
        filename = request.data.get("filename")
        content_type = request.data.get("content_type")

        if not filename or not content_type:
            return Response(
                {"detail": "filename and content_type are required"},
                status=400,
            )

        tenant = request.tenant
        url_data = generate_presigned_upload_url(
            filename=filename,
            tenant_schema=tenant.schema_name,
            content_type=content_type,
        )

        return Response(url_data)
