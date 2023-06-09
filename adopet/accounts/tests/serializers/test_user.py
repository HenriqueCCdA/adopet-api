import pytest

from adopet.accounts.models import CustomUser as User
from adopet.accounts.serializers import UserSerializer

pytestmark = pytest.mark.django_db


def test_positive_metadata_fields():
    serializer = UserSerializer()

    assert serializer.fields["name"].max_length == 120
    assert serializer.fields["email"].max_length == 254

    assert serializer.fields["password"].max_length == 128
    assert serializer.fields["password"].write_only

    assert serializer.fields["password2"].max_length == 128
    assert serializer.fields["password2"].write_only

    assert serializer.fields["created_at"].read_only
    assert serializer.fields["modified_at"].read_only


def test_positive_create(create_tutor_payload):
    serializer = UserSerializer(data=create_tutor_payload)

    assert serializer.is_valid()

    tutor = serializer.save()
    assert User.objects.exists()

    assert tutor.check_password(create_tutor_payload["password"])


def test_negative_password2_must_be_equal_password(create_tutor_payload):
    create_tutor_payload["password2"] = create_tutor_payload["password"] + "!!"

    serializer = UserSerializer(data=create_tutor_payload)

    assert not serializer.is_valid()

    assert serializer.errors["non_field_errors"] == ["Password não são iguais."]


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

    serializer = UserSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors["password"] == errors


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

    serializer = UserSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == errors
