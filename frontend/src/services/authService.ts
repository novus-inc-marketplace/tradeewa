import axios from 'axios';

const API_URL = 'http://localhost:8000';

const signup = (email, password) => {
  return axios.post(`${API_URL}/users/`, {
    email,
    password,
  });
};

const login = (email, password) => {
  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', password);
  return axios.post(`${API_URL}/token`, params);
};

const verifyEmail = (token: string) => {
  return axios.get(`${API_URL}/verify-email/${token}`);
};

export default {
  signup,
  login,
  verifyEmail,
};
