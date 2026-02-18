import requests
import os

class LinkedInPublisher:
    def __init__(self, token):
        self.token = token
        # Using 202602 as confirmed by your previous successful handshake
        self.version = "202602" 
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "LinkedIn-Version": self.version,
            "X-Restli-Protocol-Version": "2.0.0"
        }

    def check_connection(self):
        """
        Performs a 'Version Probe' to verify the API version and token 
        without needing Partner-level permissions.
        """
        print(f"🔍 Probing LinkedIn API Version ({self.version})...")
        
        # 1. First, validate the token using the OpenID endpoint (no version needed)
        token_check = requests.get(
            "https://api.linkedin.com/v2/userinfo", 
            headers={"Authorization": f"Bearer {self.token}"}
        )
        if token_check.status_code != 200:
            return False, "Access Token is invalid or expired. Please refresh it."

        # 2. Second, probe the versioned Posts API with an empty request.
        # This will return 400 (Bad Request) if the version is valid,
        # or 426 (Nonexistent Version) if the version is wrong.
        probe_url = "https://api.linkedin.com/rest/posts"
        probe_res = requests.post(probe_url, headers=self.headers, json={})
        
        if probe_res.status_code == 426:
            return False, f"Version {self.version} is not active. Try '202601' or check the developer portal."
        
        # 400 means 'I heard you and I accept your version, but your data was empty.' 
        # This is exactly what we want for a successful handshake!
        if probe_res.status_code in [400, 422]: 
            print("✅ LinkedIn Handshake Successful (Version Verified).")
            return True, None
            
        return False, f"Unexpected LinkedIn response: {probe_res.status_code}"

    def get_my_urn(self):
        # Uses the accessible OpenID endpoint to get your personal ID
        response = requests.get(
            "https://api.linkedin.com/v2/userinfo", 
            headers={"Authorization": f"Bearer {self.token}"}
        )
        return response.json().get('sub')

    def post(self, text):
        author_id = self.get_my_urn()
        url = "https://api.linkedin.com/rest/posts"
        payload = {
            "author": f"urn:li:person:{author_id}",
             "lifecycleState": "PUBLISHED", 
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {"feedDistribution": "MAIN_FEED"}
        }
        return requests.post(url, json=payload, headers=self.headers)