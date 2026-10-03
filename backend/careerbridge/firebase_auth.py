import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings


def get_firebase_app():
    """
    Initialize Firebase Admin SDK once and reuse the same app.
    """

    if firebase_admin._apps:
        return firebase_admin.get_app()

    configured_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")

    if not configured_path:
        raise RuntimeError(
            "FIREBASE_SERVICE_ACCOUNT_PATH is not configured."
        )

    credential_path = Path(settings.BASE_DIR) / configured_path

    if not credential_path.exists():
        raise RuntimeError(
            f"Firebase service account file not found: {credential_path}"
        )

    credential = credentials.Certificate(str(credential_path))

    return firebase_admin.initialize_app(credential)


def verify_firebase_token(id_token):
    """
    Verify a Firebase ID token and return the decoded Firebase user data.
    """

    app = get_firebase_app()

    return auth.verify_id_token(
        id_token,
        app=app
    )