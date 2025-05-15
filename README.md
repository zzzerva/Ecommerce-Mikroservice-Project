# E-Ticaret Mikroservis Projesi

Bu proje, kullanıcı yönetimi ve ürün yönetimi için ayrı servisler içeren mikroservis tabanlı bir e-ticaret uygulamasıdır.

## Proje Yapısı

```
ecommerce/
├── docker-compose.yml
├── user_service/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── roles.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── auth.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── product_service/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── products.py
│   │   │       │   ├── cart.py
│   │   │       │   └── orders.py
│   │   │       └── api.py
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/
    ├── src/
    ├── public/
    ├── package.json
    └── Dockerfile
```

## Kullanılan Teknolojiler

### Kullanıcı Servisi (User Service)
- **FastAPI**: Modern, hızlı API geliştirme çerçevesi
- **SQLAlchemy**: SQL ORM kütüphanesi
- **PostgreSQL**: İlişkisel veritabanı
- **Pydantic**: Veri doğrulama ve ayarlar yönetimi
- **Uvicorn**: ASGI web sunucusu
- **JWT**: Kimlik doğrulama için JSON Web Token
- **Docker**: Konteynerizasyon

### Ürün Servisi (Product Service)
- **FastAPI**: API geliştirme çerçevesi
- **SQLAlchemy**: ORM kütüphanesi
- **SQLite**: Yerel veritabanı
- **Pydantic**: Veri doğrulama
- **Docker**: Konteynerizasyon

### Ön Yüz (Frontend)
- **React**: Kullanıcı arayüzü kütüphanesi
- **React Router**: Sayfa yönlendirme
- **Docker**: Konteynerizasyon

## Kurulum ve Çalıştırma Adımları

### Önkoşullar
- Docker ve Docker Compose yüklü olmalı
- Git

### Adımlar

1. Projeyi klonlayın:
   ```bash
   git clone <repo-url>
   cd ecommerce
   ```

2. Docker Compose ile tüm servisleri başlatın:
   ```bash
   docker-compose up -d
   ```

3. Servisler aşağıdaki adreslerde çalışacaktır:
   - Frontend: http://localhost:3000
   - Kullanıcı Servisi API: http://localhost:8007
   - Ürün Servisi API: http://localhost:8001/api/v1
   - Kullanıcı Servisi API Belgeleri: http://localhost:8007/docs
   - Ürün Servisi API Belgeleri: http://localhost:8001/docs

### Geliştirme Ortamı Kurulumu

Eğer servisleri ayrı ayrı geliştirmek isterseniz:

1. PostgreSQL veritabanını başlatın:
   ```bash
   docker-compose up -d db
   ```

2. Kullanıcı Servisi için sanal ortam kurun:
   ```bash
   cd user_service
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Kullanıcı Servisini çalıştırın:
   ```bash
   uvicorn app.main:app --reload --port 8007
   ```

4. Ürün Servisi için sanal ortam kurun:
   ```bash
   cd product_service
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. Ürün Servisini çalıştırın:
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

6. Frontend geliştirme sunucusunu başlatın:
   ```bash
   cd frontend
   npm install
   npm start
   ```

## API Endpoint Listesi

### Kullanıcı Servisi (User Service) Endpoints

#### Kimlik Doğrulama (Authentication)
- `POST /login` - Kullanıcı girişi, JWT token döndürür
- `POST /logout` - Kullanıcının token'ını geçersiz kılar
- `GET /check-login` - Token'ın geçerli olup olmadığını kontrol eder
- `GET /user-info` - Giriş yapmış kullanıcının bilgilerini getirir
- `GET /protected-route` - Korumalı bir rota örneği
- `GET /admin-dashboard` - Sadece admin erişimli dashboard

#### Kullanıcı Yönetimi (User Management)
- `POST /users/` - Yeni bir kullanıcı oluşturur
- `GET /users/me` - Mevcut kullanıcı detaylarını getirir
- `GET /users/` - Tüm kullanıcıları listeler (Sadece Admin)
- `GET /users/{user_id}` - Belirli bir kullanıcının detaylarını getirir (Sadece Admin)
- `PUT /users/{user_id}` - Kullanıcı detaylarını günceller (Sadece Admin)
- `DELETE /users/{user_id}` - Bir kullanıcıyı siler (Sadece Admin)
- `PUT /users/me/password` - Kendi şifresini değiştirir
- `PUT /users/{user_id}/password/reset` - Kullanıcının şifresini sıfırlar (Sadece Admin)
- `PUT /users/{user_id}/status` - Kullanıcının aktif durumunu günceller (Sadece Admin)
- `PUT /users/me/deactivate` - Kendi hesabını devre dışı bırakır

#### Adres Yönetimi (Address Management)
- `POST /users/me/addresses` - Yeni bir adres ekler
- `PUT /users/me/addresses/{address_id}` - Bir adresi günceller
- `DELETE /users/me/addresses/{address_id}` - Bir adresi siler

#### İletişim Yönetimi (Contact Management)
- `POST /users/me/contacts` - Yeni bir iletişim bilgisi ekler

#### Rol Yönetimi (Role Management)
- `POST /roles` - Yeni bir rol oluşturur (Sadece Admin)
- `PUT /roles/{role_id}` - Bir rolü günceller (Sadece Admin)
- `POST /roles/{role_id}/permissions` - Bir role yetki ekler (Sadece Admin)

### Ürün Servisi (Product Service) Endpoints

#### Ürünler (Products)
- `GET /api/v1/products` - Tüm ürünleri listeler
- `GET /api/v1/products/{product_id}` - Belirli bir ürünün detaylarını getirir
- `POST /api/v1/products` - Yeni bir ürün oluşturur (Admin)
- `PUT /api/v1/products/{product_id}` - Bir ürünü günceller (Admin)
- `DELETE /api/v1/products/{product_id}` - Bir ürünü siler (Admin)

#### Sepet (Cart)
- `GET /api/v1/cart` - Kullanıcının sepetini getirir
- `POST /api/v1/cart/items` - Sepete ürün ekler
- `PUT /api/v1/cart/items/{item_id}` - Sepetteki bir ürünün miktarını günceller
- `DELETE /api/v1/cart/items/{item_id}` - Sepetten bir ürünü kaldırır

#### Siparişler (Orders)
- `GET /api/v1/orders` - Kullanıcının tüm siparişlerini listeler
- `GET /api/v1/orders/{order_id}` - Belirli bir siparişin detaylarını getirir
- `POST /api/v1/orders` - Yeni bir sipariş oluşturur
- `PUT /api/v1/orders/{order_id}/status` - Bir siparişin durumunu günceller (Admin)

## Varsayılan Admin Kullanıcı Bilgileri

Sistem ilk başlatıldığında aşağıdaki varsayılan admin kullanıcısı oluşturulur:

- **Kullanıcı Adı**: admin
- **Şifre**: admin123
- **Rol**: Admin

**Önemli Not**: Güvenlik nedeniyle ilk giriş sonrası admin şifresini değiştirmeniz önerilir. 
