import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import Profile from './pages/Profile';
import Orders from './pages/Orders';
import Checkout from './pages/Checkout';
import Payment from './pages/Payment';
import Admin from './pages/Admin';

const AppRoutes = () => (
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/login" element={<Login />} />
    <Route path="/register" element={<Register />} />
    <Route path="/forgot-password" element={<ForgotPassword />} />
    <Route path="/profile" element={<Profile />} />
    <Route path="/orders" element={<Orders />} />
    <Route path="/checkout" element={<Checkout />} />
    <Route path="/payment" element={<Payment />} />
    <Route path="/admin" element={<Admin />} />
    {/* Diğer sayfalar buraya eklenecek */}
  </Routes>
);

export default AppRoutes; 