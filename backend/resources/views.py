from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import CommunityResource
from .serializers import CommunityResourceSerializer


class CommunityResourceListCreateView(APIView):
    """GET /api/resources/?skill=python  -> resources the community has
    shared for that skill (visible to every user, not just the submitter).
    POST /api/resources/  -> share a new link for a skill.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        skill = request.query_params.get("skill", "").strip()

        queryset = CommunityResource.objects.all()
        if skill:
            queryset = queryset.filter(skill__iexact=skill)

        serializer = CommunityResourceSerializer(queryset[:20], many=True)
        return Response({"resources": serializer.data})

    def post(self, request):
        skill = request.data.get("skill", "").strip()
        title = request.data.get("title", "").strip()
        url = request.data.get("url", "").strip()

        if not skill or not title or not url:
            return Response(
                {"error": "skill, title and url are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not (url.startswith("http://") or url.startswith("https://")):
            return Response(
                {"error": "url must start with http:// or https://"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        resource = CommunityResource.objects.create(
            skill=skill,
            title=title,
            url=url,
            note=request.data.get("note", "").strip(),
            resource_type=request.data.get("resource_type", "other"),
            submitted_by=request.user,
        )

        serializer = CommunityResourceSerializer(resource)
        return Response(
            {"message": "Thanks — your resource is now visible to everyone learning this skill.", "resource": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class CommunityResourceUpvoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resource_id):
        try:
            resource = CommunityResource.objects.get(id=resource_id)
        except CommunityResource.DoesNotExist:
            return Response({"error": "Resource not found."}, status=status.HTTP_404_NOT_FOUND)

        resource.upvotes += 1
        resource.save(update_fields=["upvotes"])

        serializer = CommunityResourceSerializer(resource)
        return Response(serializer.data)
