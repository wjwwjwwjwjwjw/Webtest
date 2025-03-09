import { useState, useEffect } from 'react';
import Head from 'next/head';
import styles from '../styles/Home.module.css';
import axios from 'axios';

export default function Home() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newItem, setNewItem] = useState('');

  // ��ȡ����
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/items');
        setItems(response.data);
        setLoading(false);
      } catch (error) {
        console.error('��ȡ����ʧ��:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // �������Ŀ
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!newItem.trim()) return;
    
    try {
      const response = await axios.post('/api/items', { name: newItem });
      setItems([...items, response.data]);
      setNewItem('');
    } catch (error) {
      console.error('�����Ŀʧ��:', error);
    }
  };

  // ɾ����Ŀ
  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/items?id=${id}`);
      setItems(items.filter(item => item.id !== id));
    } catch (error) {
      console.error('ɾ����Ŀʧ��:', error);
    }
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>Web����ϵͳ</title>
        <meta name="description" content="Web����ϵͳ" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>Web����ϵͳ</h1>
        
        <p className={styles.description}>
          ��������Web��Ŀ
        </p>

        <div className={styles.formContainer}>
          <form onSubmit={handleSubmit} className={styles.form}>
            <input
              type="text"
              value={newItem}
              onChange={(e) => setNewItem(e.target.value)}
              placeholder="������Ŀ����..."
              className={styles.input}
            />
            <button type="submit" className={styles.button}>���</button>
          </form>
        </div>

        <div className={styles.grid}>
          {loading ? (
            <p>������...</p>
          ) : items.length === 0 ? (
            <p>������Ŀ�������</p>
          ) : (
            items.map((item) => (
              <div key={item.id} className={styles.card}>
                <h2>{item.name}</h2>
                <button 
                  onClick={() => handleDelete(item.id)}
                  className={styles.deleteButton}
                >
                  ɾ��
                </button>
              </div>
            ))
          )}
        </div>
      </main>

      <footer className={styles.footer}>
        <a
          href="https://vercel.com"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by Vercel
        </a>
      </footer>
    </div>
  );
} 