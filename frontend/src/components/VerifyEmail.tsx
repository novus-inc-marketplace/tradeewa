import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import authService from '../services/authService';

const VerifyEmail: React.FC = () => {
  const { token } = useParams<{ token: string }>();
  const [message, setMessage] = useState('Verifying email...');

  useEffect(() => {
    const verifyUserEmail = async () => {
      try {
        if (token) {
          await authService.verifyEmail(token);
          setMessage('Email verified successfully! You can now log in.');
        } else {
          setMessage('Invalid verification link: Token not found.');
        }
      } catch (error) {
        setMessage('Email verification failed. The link might be invalid or expired.');
      }
    };

    verifyUserEmail();
  }, [token]);

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
      <div className="p-8 bg-gray-800 rounded-lg shadow-md text-center">
        <h2 className="text-2xl font-bold mb-4">Email Verification</h2>
        <p>{message}</p>
      </div>
    </div>
  );
};

export default VerifyEmail;
