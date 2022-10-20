import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { API_URL } from '../utils'

export const deviceManagerApi = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: `${API_URL}` }),
  tagTypes: [],
  endpoints: (builder) => ({
    getOverview: builder.query({
      query: () => `overview`,
    }),
    getDevices: builder.query({
      query: () => `devices`,
    }),
    getDevice: builder.query({
      query: (id: number) => `devices/${id}`,
    }),
    getMessages: builder.query({
      query: () => `messages`,
    }),
    uploadConfigFile: builder.mutation({
      query(body) {
        return {
          url: `uploadConfig`,
          method: "POST",
          body,
        };
      },
    }),
  }),
})

// Export hooks for usage in functional components
export const { useGetOverviewQuery, useGetDevicesQuery, useGetDeviceQuery, useGetMessagesQuery, useUploadConfigFileMutation } = deviceManagerApi