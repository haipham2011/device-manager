import { createSlice } from '@reduxjs/toolkit'

export const messageSlice = createSlice({
    name: 'overview',
    initialState: {
        value: 0,
    },
    reducers: {
        increment: state => {
            state.value += 1
        }
    }
})

export const { increment } = messageSlice.actions

export default messageSlice.reducer