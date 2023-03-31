import pytest

from adopet.core.models import CustomUser as User
from adopet.core.serializers import TutorSerializer

pytestmark = pytest.mark.django_db


def test_positive_serialization_objs_list(users):
    serialize = TutorSerializer(instance=User.objects.all(), many=True)

    for data, db in zip(serialize.data, users):
        assert data["id"] == db.id
        assert data["name"] == db.name
        assert data["email"] == db.email
        assert "password" not in data
        assert "password2" not in data
        assert data["is_active"] == db.is_active
        assert data["created_at"] == str(db.created_at.astimezone().isoformat())
        assert data["modified_at"] == str(db.modified_at.astimezone().isoformat())


def test_positive_serialization_one_obj(users):
    tutor = users[2]

    serialize = TutorSerializer(instance=tutor)

    data = serialize.data

    assert data["id"] == tutor.id
    assert data["name"] == tutor.name
    assert data["email"] == tutor.email
    assert "password" not in data
    assert "password2" not in data
    assert data["is_active"] == tutor.is_active
    assert data["created_at"] == str(tutor.created_at.astimezone().isoformat())
    assert data["modified_at"] == str(tutor.modified_at.astimezone().isoformat())


def test_positive_metadata_fields():
    serialize = TutorSerializer()

    assert serialize.fields["name"].max_length == 120
    assert serialize.fields["email"].max_length == 254

    assert serialize.fields["password"].max_length == 128
    assert serialize.fields["password"].write_only

    assert serialize.fields["password2"].max_length == 128
    assert serialize.fields["password2"].write_only

    assert serialize.fields["created_at"].read_only
    assert serialize.fields["modified_at"].read_only


def test_positive_create_user(create_tutor_payload):
    serialize = TutorSerializer(data=create_tutor_payload)

    assert serialize.is_valid()

    tutor = serialize.save()

    assert User.objects.exists()

    assert tutor.check_password(create_tutor_payload["password"])


def test_negative_password2_must_be_equal_password(create_tutor_payload):
    create_tutor_payload["password2"] = create_tutor_payload["password"] + "!!"

    serialize = TutorSerializer(data=create_tutor_payload)

    assert not serialize.is_valid()

    assert serialize.errors["non_field_errors"] == ["Password não são iguais."]


@pytest.mark.parametrize(
    "password, errors",
    [
        (
            "1",
            [
                "Esta senha é muito curta. Ela precisa conter pelo menos 8 caracteres.",
                "Esta senha é muito comum.",
                "Esta senha é inteiramente numérica.",
            ],
        ),
        ("12345678", ["Esta senha é muito comum.", "Esta senha é inteiramente numérica."]),
        ("abcd1234", ["Esta senha é muito comum."]),
    ],
)
def test_negative_password_validation(password, errors, create_tutor_payload):
    data = create_tutor_payload.copy()

    data["password"] = password
    data["password2"] = password

    serialize = TutorSerializer(data=data)

    assert not serialize.is_valid()

    assert serialize.errors["password"] == errors


@pytest.mark.parametrize(
    "field, errors",
    [
        ("name", ["Este campo é obrigatório."]),
        ("email", ["Este campo é obrigatório."]),
        ("password", ["Este campo é obrigatório."]),
        ("password2", ["Este campo é obrigatório."]),
    ],
)
def test_negative_missing_fields(field, errors, create_tutor_payload):
    data = create_tutor_payload.copy()

    del data[field]

    serialize = TutorSerializer(data=data)

    assert not serialize.is_valid()

    assert serialize.errors[field] == errors
