
window.onload = function() {
  // Build a system
  var url = window.location.search.match(/url=([^&]+)/);
  if (url && url.length > 1) {
    url = decodeURIComponent(url[1]);
  } else {
    url = window.location.origin;
  }
  var options = {
  "swaggerDoc": {
    "info": {
      "title": "Silk APIs Swagger documentation",
      "version": "0.1.0",
      "description": "Mocked up API for Silk Interviews. You will find endpoints for Qualys/Crowdstrike, which return raw data from those tools. Good luck!",
      "contact": {
        "name": "Silk",
        "url": "https://www.silk.security",
        "email": "support@silk.security"
      }
    },
    "securityDefinitions": {
      "authToken": {
        "type": "apiKey",
        "in": "header",
        "name": "token"
      }
    },
    "security": {
      "authToken": []
    },
    "servers": [
      {
        "url": "http://api.recruiting.app.silk.security:80"
      }
    ],
    "swagger": "2.0",
    "paths": {
      "/api/qualys/hosts/get": {
        "post": {
          "tags": [
            "Qualys"
          ],
          "security": [
            {
              "authToken": []
            }
          ],
          "summary": "Get qualys scanned hosts",
          "description": "Get all qualys scanned hosts, using query parameter pagination",
          "parameters": [
            {
              "in": "query",
              "name": "skip",
              "schema": {
                "type": "integer"
              },
              "required": true,
              "default": 0,
              "description": "how many hosts to skip"
            },
            {
              "in": "query",
              "name": "limit",
              "schema": {
                "type": "integer"
              },
              "required": true,
              "default": 1,
              "description": "how many hosts to fetch"
            }
          ],
          "responses": {
            "200": {
              "description": "Success - returns a list of all scanned hosts"
            }
          }
        }
      },
      "/api/crowdstrike/hosts/get": {
        "post": {
          "tags": [
            "Crowdstrike"
          ],
          "security": [
            {
              "authToken": []
            }
          ],
          "summary": "Get Crowdstrike scanned hosts",
          "description": "Get all Crowdstrike scanned hosts, using query parameter pagination",
          "parameters": [
            {
              "in": "query",
              "name": "skip",
              "schema": {
                "type": "integer"
              },
              "required": true,
              "default": 0,
              "description": "how many hosts to skip"
            },
            {
              "in": "query",
              "name": "limit",
              "schema": {
                "type": "integer"
              },
              "required": true,
              "default": 1,
              "description": "how many hosts to fetch"
            }
          ],
          "responses": {
            "200": {
              "description": "Success - returns a list of all scanned hosts"
            }
          }
        }
      }
    },
    "definitions": {},
    "responses": {},
    "parameters": {},
    "tags": []
  },
  "customOptions": {},
  "swaggerUrl": {}
};
  url = options.swaggerUrl || url
  var urls = options.swaggerUrls
  var customOptions = options.customOptions
  var spec1 = options.swaggerDoc
  var swaggerOptions = {
    spec: spec1,
    url: url,
    urls: urls,
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ],
    layout: "StandaloneLayout"
  }
  for (var attrname in customOptions) {
    swaggerOptions[attrname] = customOptions[attrname];
  }
  var ui = SwaggerUIBundle(swaggerOptions)

  if (customOptions.oauth) {
    ui.initOAuth(customOptions.oauth)
  }

  if (customOptions.preauthorizeApiKey) {
    const key = customOptions.preauthorizeApiKey.authDefinitionKey;
    const value = customOptions.preauthorizeApiKey.apiKeyValue;
    if (!!key && !!value) {
      const pid = setInterval(() => {
        const authorized = ui.preauthorizeApiKey(key, value);
        if(!!authorized) clearInterval(pid);
      }, 500)

    }
  }

  if (customOptions.authAction) {
    ui.authActions.authorize(customOptions.authAction)
  }

  window.ui = ui
}
