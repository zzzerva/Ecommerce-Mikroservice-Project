import React, { createContext, useContext, useState, useCallback } from 'react';

const OrderContext = createContext();

export const OrderProvider = ({ children }) => {
  const [orders, setOrders] = useState([]);

  const addOrder = useCallback((order) => {
    setOrders(prevOrders => [order, ...prevOrders]);
  }, []);

  const getOrders = useCallback(() => {
    return orders;
  }, [orders]);

  return (
    <OrderContext.Provider value={{
      orders,
      addOrder,
      getOrders
    }}>
      {children}
    </OrderContext.Provider>
  );
};

export const useOrder = () => {
  const context = useContext(OrderContext);
  if (!context) {
    throw new Error('useOrder must be used within an OrderProvider');
  }
  return context;
}; 