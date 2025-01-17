// @ts-check

import { test, expect, type Page } from '@playwright/test';

test("Creating a Odoo user", async ({request}) => {
    const response = await request.post("http://localhost:8000/api/users/", {
        data: {
            username: "newuser1",
            email: "newuser1@email.com",
            password: "136900"
        }
    })

    console.log(await response.json());
    expect(response.status()).toBe(201);
    // const responseBody = await response.json();
    // expect(responseBody.message).toHaveProperty("firstname", "Jim");
})