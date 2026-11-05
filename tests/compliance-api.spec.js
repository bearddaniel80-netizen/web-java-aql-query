import { test, expect } from "@playwright/test"

const BASE_URL = "http://node";

test.describe("Express API routes", () => {

  test("GET /api/manifest/list", async ({ request }) => {
    const response = await request.get(
      `${BASE_URL}/api/manifest/list`
    );

    expect(response.status()).toBe(200);
  });

  test("GET /api/suite/list", async ({ request }) => {
    const response = await request.get(
      `${BASE_URL}/api/suite/list`
    );

    expect(response.status()).toBe(200);
  });

  test("GET /api/tag/list", async ({ request }) => {
    const response = await request.get(
      `${BASE_URL}/api/tag/list`
    );

    expect(response.status()).toBe(200);
  });

  test("GET /api/manifest/profile/:filename", async ({ request }) => {
    const filename = "csv";

    const response = await request.get(
      `${BASE_URL}/api/manifest/profile/${filename}`
    );

    expect(response.status()).toBe(200);
  });

  test("GET /api/suite/profile/:filename", async ({ request }) => {
    const filename = "core";

    const response = await request.get(
      `${BASE_URL}/api/suite/profile/${filename}`
    );

    expect(response.status()).toBe(200);
  });

  test("GET /api/tag/profile/:tag", async ({ request }) => {
    const tag = "csv";

    const response = await request.get(
      `${BASE_URL}/api/tag/profile/${tag}`
    );

    expect(response.status()).toBe(200);

  });

  test("GET /api/manifest/:filename", async ({ request }) => {
    const filename = "csv";

    const response = await request.get(
      `${BASE_URL}/api/manifest/${filename}`
    );

    expect(response.status()).toBe(200);
  });

  test("GET /api/suite/:filename", async ({ request }) => {
    const filename = "core";

    const response = await request.get(
      `${BASE_URL}/api/suite/${filename}`
    );

    expect(response.status()).toBe(200);
  });

  test("GET /api/tag/:tag", async ({ request }) => {
    const tag = "csv";

    const response = await request.get(
      `${BASE_URL}/api/tag/${tag}`
    );

    expect(response.status()).toBe(200);

  });
});