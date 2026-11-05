import { readFileSync } from "fs";
import multer from "multer";

function readSecret(name) {
  const path = `/run/secrets/${name}`;

  try {
    return readFileSync(path, "utf8").trim();
  } catch (err) {
    console.error(`Could not read secret: ${path}`);
    process.exit(1);
  }
}

const FASTAPI_URL = process.env.FASTAPI_URL;
const FASTAPI_INTERNAL_KEY = readSecret("fastapi_internal_key");

export const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 100 * 1024 * 1024,
  },
});
export async function get_fastapi(
  path,
  {
    body,
    headers = {},
  } = {}
) {
  const response = await fetch(
    `${FASTAPI_URL}${path}`,
    {
      method: "GET",

      headers: {
        "X-Internal-Key": FASTAPI_INTERNAL_KEY,
        "Accept": "application/json",

        ...(body !== undefined
          ? {
              "Content-Type": "application/json",
            }
          : {}),

        ...headers,
      },

      ...(body !== undefined
        ? {
            body: JSON.stringify(body),
          }
        : {}),
    }
  );

  return parseResponse(response);
}

export async function post_fastapi(
  path,
  {
    body,
    headers = {},
  } = {}
) {
  const response = await fetch(
    `${FASTAPI_URL}${path}`,
    {
      method: "POST",

      headers: {
        "X-Internal-Key": FASTAPI_INTERNAL_KEY,
        "Accept": "application/json",

        ...(body !== undefined
          ? {
              "Content-Type": "application/json",
            }
          : {}),

        ...headers,
      },

      ...(body !== undefined
        ? {
            body: JSON.stringify(body),
          }
        : {}),
    }
  );

  return parseResponse(response);
}
export async function upload_to_fastapi(
  path,
  file,
  fields = {}
) {
  const body = {
    filename: file.originalname,
    content_type: file.mimetype,
    ...fields,
  };

  const response = await fetch(
    `${FASTAPI_URL}${path}`,
    {
      method: "POST",

      headers: {
        "X-Internal-Key": FASTAPI_INTERNAL_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json",
      },

      body: JSON.stringify(body),
    }
  );

  return parseResponse(response);
}

async function parseResponse(response) {
  let data = null;

  const contentType =
    response.headers.get("content-type");

  if (contentType?.includes("application/json")) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  return {
    status: response.status,
    ok: response.ok,
    data,
  };
}