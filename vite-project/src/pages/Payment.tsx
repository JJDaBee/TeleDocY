import React, { useEffect, useState } from 'react';
import Navbar from '../components/navbar';
import Footer from '../components/footer';

const stripeCheckoutUrl = 'http://localhost:5300/settle_payment'; // Update this to your actual payment composite URL

type Payment = {
    paymentID: number;
    amount: number;
    datetime: string;
};

const PaymentPage: React.FC = () => {
    const [payments, setPayments] = useState<Payment[]>([]);
    const [uuid, setUuid] = useState<string>('');

    useEffect(() => {
        const storedUser = sessionStorage.getItem('loggedInUser');
        if (storedUser) {
            try {
                const parsedUser = JSON.parse(storedUser);
                const uuid = parsedUser?.uuid;

                if (uuid) {
                    setUuid(uuid);
                    fetchPaymentsByUuid(uuid);
                } else {
                    console.warn('⚠️ UUID not found in stored user.');
                }
            } catch (error) {
                console.error('❌ Failed to parse user from storage:', error);
            }
        } else {
            console.warn('⚠️ No user found in storage.');
        }
    }, []);

    const fetchPaymentsByUuid = async (uuid: string) => {
        try {
            const res = await fetch(
                `http://localhost:5009/payments/uuid/${uuid}`
            );
            const data = await res.json();
            setPayments(data.data || []);
        } catch (err) {
            console.error('❌ Error fetching payments by UUID:', err);
        }
    };

    const handlePay = async (paymentID: number) => {
        try {
            const res = await fetch(stripeCheckoutUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ paymentID, uuid }),
            });

            const data = await res.json();

            if (res.ok && data.stripe_checkout_url) {
                window.open(data.stripe_checkout_url, '_blank'); // open Stripe checkout in new tab
            } else {
                alert(
                    `Failed to create checkout: ${
                        data.message || 'Unknown error'
                    }`
                );
                console.error('❌ Stripe error:', data);
            }
        } catch (error) {
            console.error('❌ Payment processing failed:', error);
            alert('Error while initiating payment.');
        }
    };

    return (
        <>
            <Navbar />
            <section
                style={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'flex-start',
                    padding: '60px 20px',
                    background: '#f9f9f9',
                    minHeight: '100vh',
                    width: '100vw',
                    boxSizing: 'border-box',
                }}
            >
                <div
                    style={{
                        width: '100%',
                        maxWidth: '1000px',
                        background: 'white',
                        borderRadius: '12px',
                        padding: '30px',
                        boxShadow: '0 0 15px rgba(0,0,0,0.05)',
                    }}
                >
                    <h2
                        style={{
                            fontSize: '2rem',
                            marginBottom: '30px',
                            color: '#333',
                        }}
                    >
                        My Payments
                    </h2>

                    {payments.length === 0 ? (
                        <p style={{ color: '#888' }}>
                            No payment records found.
                        </p>
                    ) : (
                        <table
                            style={{
                                width: '100%',
                                borderCollapse: 'collapse',
                                fontSize: '1rem',
                            }}
                        >
                            <thead>
                                <tr>
                                    <th style={tableHeaderStyle}>Payment ID</th>
                                    <th style={tableHeaderStyle}>
                                        Amount (SGD)
                                    </th>
                                    <th style={tableHeaderStyle}>Date</th>
                                    <th style={tableHeaderStyle}>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {payments.map((payment) => (
                                    <tr key={payment.paymentID}>
                                        <td style={tableCellStyle}>
                                            {payment.paymentID}
                                        </td>
                                        <td style={tableCellStyle}>
                                            ${payment.amount.toFixed(2)}
                                        </td>
                                        <td style={tableCellStyle}>
                                            {payment.datetime}
                                        </td>
                                        <td style={tableCellStyle}>
                                            <button
                                                style={buttonStyle}
                                                onClick={() =>
                                                    handlePay(payment.paymentID)
                                                }
                                            >
                                                Pay
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>
            </section>
            <Footer />
        </>
    );
};

const tableHeaderStyle: React.CSSProperties = {
    textAlign: 'left',
    paddingBottom: '10px',
    borderBottom: '2px solid #ddd',
    color: '#333',
};

const tableCellStyle: React.CSSProperties = {
    padding: '12px 10px',
    borderBottom: '1px solid #eee',
    color: '#555',
};

const buttonStyle: React.CSSProperties = {
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    padding: '8px 16px',
    borderRadius: '6px',
    cursor: 'pointer',
};

export default PaymentPage;
