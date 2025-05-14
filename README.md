# User Service - E-Commerce Mikroservice

Bu proje, e-commerce uygulamasının kullanıcı yönetiminden sorumlu mikroservisidir. Kullanıcı kaydı, kimlik doğrulaması, profil yönetimi, adres ve iletişim bilgilerini yönetir.

## 🚀 Teknolojiler

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Bcrypt
- **Validation**: Pydantic
- **Testing**: Pytest
- **Database Migrations**: Alembic

## 📋 Ön Gereksinimler

- Python 3.8+
- PostgreSQL
- pip

## 🔧 Kurulum ve Çalıştırma

### 1. Projeyi Klonlayın

```bash
git clone <repository-url>
cd user_service
```

### 2. Virtual Environment Oluşturun

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Ayarlayın

`.env` dosyası oluşturun:

```env
# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345
POSTGRES_DB=user_service
POSTGRES_PORT=5432

# JWT
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
PROJECT_NAME="User Service"
VERSION="1.0.0"
API_V1_STR="/api/v1"
```

### 5. Veritabanını Oluşturun

```bash
# PostgreSQL'de veritabanı oluştur
createdb user_service

# Migration'ları çalıştır
alembic upgrade head
```

### 6. Uygulamayı Başlatın

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Uygulama http://localhost:8000 adresinde çalışmaya başlar.

## 📚 API Endpoints

### Auth Endpoints

- `POST /api/v1/auth/register` - Kullanıcı kaydı
- `POST /api/v1/auth/login` - Kullanıcı girişi
- `POST /api/v1/auth/refresh` - Token yenileme

### User Endpoints

- `GET /api/v1/users/me` - Mevcut kullanıcı bilgilerini getir
- `PUT /api/v1/users/me` - Kullanıcı bilgilerini güncelle
- `GET /api/v1/users/{user_id}` - Belirli kullanıcıyı getir (Admin)
- `GET /api/v1/users/` - Tüm kullanıcıları listele (Admin)
- `PUT /api/v1/users/{user_id}` - Kullanıcı güncelle (Admin)
- `DELETE /api/v1/users/{user_id}` - Kullanıcı sil (Admin)

### Address Endpoints

- `POST /api/v1/address/` - Adres oluştur
- `GET /api/v1/address/` - Kullanıcının adreslerini listele
- `GET /api/v1/address/{address_id}` - Belirli adres getir
- `PUT /api/v1/address/{address_id}` - Adres güncelle
- `DELETE /api/v1/address/{address_id}` - Adres sil
- `GET /api/v1/address/user/me` - Mevcut kullanıcının adresleri
- `GET /api/v1/address/user/{user_id}` - Kullanıcının adresleri (Admin)

### Contact Endpoints

- `POST /api/v1/contact/` - İletişim bilgisi oluştur
- `GET /api/v1/contact/` - Kullanıcının iletişim bilgilerini listele
- `GET /api/v1/contact/{contact_id}` - Belirli iletişim bilgisi getir
- `PUT /api/v1/contact/{contact_id}` - İletişim bilgisi güncelle
- `DELETE /api/v1/contact/{contact_id}` - İletişim bilgisi sil
- `GET /api/v1/contact/user/me` - Mevcut kullanıcının iletişim bilgileri
- `GET /api/v1/contact/user/{user_id}` - Kullanıcının iletişim bilgileri (Admin)

## 👤 Varsayılan Admin Kullanıcı

İlk çalıştırmada varsayılan admin kullanıcısı otomatik olarak oluşturulur:

- **Email**: admin@example.com
- **Password**: admin123
- **Username**: admin
- **Role**: Superuser

## 📊 API Dokümantasyonu

Uygulama çalışırken aşağıdaki URL'lerden interaktif API dokümantasyonuna erişebilirsiniz:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testler

Testleri çalıştırmak için:

```bash
# Tüm testleri çalıştır
pytest

# Coverage raporu ile
pytest --cov=app

# Belirli test dosyasını çalıştır
pytest tests/test_user.py
```

