from adopet.core.models import CustomUser as User
from adopet.core.serializers import TutorListSerializer


def test_serializer(users):
    serialize = TutorListSerializer(instance=User.objects.all(), many=True)

    for s, db in zip(serialize.data, users):
        assert s["id"] == db.id
        assert s["name"] == db.name
        assert s["email"] == db.email
        assert s["created_at"] == str(db.created_at.astimezone().isoformat())
        assert s["modified_at"] == str(db.modified_at.astimezone().isoformat())
