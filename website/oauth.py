import google_auth_oauthlib.flow


def get_flow():
    '''build flow'''
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'secrets/client_secret_344754237425-kk24ona4vt4472957stkabd4snpoanmv.apps.googleusercontent.com.json',
        scopes=['https://www.googleapis.com/auth/fitness.sleep.read'])

    flow.redirect_uri = 'https://127.0.0.1:5000/fit-oauth-callback'

    return flow


def get_auth_url():
    '''build authorization request'''

    flow = get_flow()

    authorization_url, state = flow.authorization_url(
        include_granted_scopes='true'
    )

    return authorization_url, state
