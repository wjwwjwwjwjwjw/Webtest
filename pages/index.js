import { useState, useEffect } from 'react';
import Head from 'next/head';
import styles from '../styles/Home.module.css';
import axios from 'axios';

export default function Home() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newItem, setNewItem] = useState('');

  // 获取数据
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/items');
        setItems(response.data);
        setLoading(false);
      } catch (error) {
        console.error('获取数据失败:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // 添加新项目
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!newItem.trim()) return;
    
    try {
      const response = await axios.post('/api/items', { name: newItem });
      setItems([...items, response.data]);
      setNewItem('');
    } catch (error) {
      console.error('添加项目失败:', error);
    }
  };

  // 删除项目
  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/items?id=${id}`);
      setItems(items.filter(item => item.id !== id));
    } catch (error) {
      console.error('删除项目失败:', error);
    }
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>Web管理系统</title>
        <meta name="description" content="Web管理系统" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>Web管理系统</h1>
        
        <p className={styles.description}>
          管理您的Web项目
        </p>

        <div className={styles.formContainer}>
          <form onSubmit={handleSubmit} className={styles.form}>
            <input
              type="text"
              value={newItem}
              onChange={(e) => setNewItem(e.target.value)}
              placeholder="输入项目名称..."
              className={styles.input}
            />
            <button type="submit" className={styles.button}>添加</button>
          </form>
        </div>

        <div className={styles.grid}>
          {loading ? (
            <p>加载中...</p>
          ) : items.length === 0 ? (
            <p>暂无项目，请添加</p>
          ) : (
            items.map((item) => (
              <div key={item.id} className={styles.card}>
                <h2>{item.name}</h2>
                <button 
                  onClick={() => handleDelete(item.id)}
                  className={styles.deleteButton}
                >
                  删除
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