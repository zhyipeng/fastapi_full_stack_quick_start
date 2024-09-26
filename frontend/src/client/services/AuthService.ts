/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_api_auth_login_post } from '../models/Body_login_api_auth_login_post';
import type { LoginRsp } from '../models/LoginRsp';
import type { RefreshReq } from '../models/RefreshReq';
import type { RefreshRsp } from '../models/RefreshRsp';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AuthService {
    /**
     * Login
     * @param formData
     * @returns LoginRsp Successful Response
     * @throws ApiError
     */
    public static loginApiAuthLoginPost(
        formData: Body_login_api_auth_login_post,
    ): CancelablePromise<LoginRsp> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/login',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Refresh
     * @param requestBody
     * @returns RefreshRsp Successful Response
     * @throws ApiError
     */
    public static refreshApiAuthRefreshPost(
        requestBody: RefreshReq,
    ): CancelablePromise<RefreshRsp> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/refresh',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
