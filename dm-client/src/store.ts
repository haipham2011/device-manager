import { configureStore, combineReducers } from "@reduxjs/toolkit";
import type { PreloadedState } from "@reduxjs/toolkit";
import { deviceManagerApi } from "./services/deviceManager";
import messageReducer from "./reducer/messageSlice";

const rootReducer = combineReducers({
  [deviceManagerApi.reducerPath]: deviceManagerApi.reducer,
  messageCounter: messageReducer
});

export const setupStore = (preloadedState?: PreloadedState<RootState>) => {
  return configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) =>
      // adding the api middleware enables caching, invalidation, polling and other features of `rtk-query`
      getDefaultMiddleware().concat(deviceManagerApi.middleware),
    preloadedState,
  });
};
// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof rootReducer>;
export type AppStore = ReturnType<typeof setupStore>;
export type AppDispatch = AppStore["dispatch"];
