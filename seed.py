"""Seed the database with sample categories and products."""
from models import db, User, Category, Product
from werkzeug.security import generate_password_hash
from app import app
from models import db, User, Category, Product
from werkzeug.security import generate_password_hash
def seed_data(app):
    with app.app_context():
        db.create_all()
        # Admin user
        if not User.query.filter_by(email="admin@markaz.pk").first():
            admin = User(
                name="Admin",
                email="admin@markaz.pk",
                phone="03001234567",
                is_admin=True
            )
            admin.set_password("admin123")
            db.session.add(admin)

        # Demo customer
        if not User.query.filter_by(email="demo@markaz.pk").first():
            demo = User(
                name="Ali Khan",
                email="demo@markaz.pk",
                phone="03219876543"
            )
            demo.set_password("demo123")
            db.session.add(demo)

        # Categories
        cats_data = [
            {"name": "Electronics", "icon": "📱", "color": "#3B82F6"},
            {"name": "Fashion", "icon": "👗", "color": "#EC4899"},
            {"name": "Beauty", "icon": "💄", "color": "#F472B6"},
            {"name": "Home", "icon": "🏠", "color": "#10B981"},
            {"name": "Men", "icon": "👔", "color": "#6366F1"},
            {"name": "Kids", "icon": "🧸", "color": "#F59E0B"},
            {"name": "Footwear", "icon": "👟", "color": "#8B5CF6"},
            {"name": "Accessories", "icon": "👜", "color": "#EF4444"},
            {"name": "Books", "icon": "📚", "color": "#14B8A6"},
            {"name": "Health", "icon": "💊", "color": "#22C55E"},
        ]
        cat_map = {}
        for c in cats_data:
            existing = Category.query.filter_by(name=c["name"]).first()
            if not existing:
                cat = Category(**c)
                db.session.add(cat)
                db.session.flush()
                cat_map[c["name"]] = cat.id
            else:
                cat_map[c["name"]] = existing.id

        db.session.commit()

        # Products
        products_data = [
            # Electronics
            {"name": "AirPods Pro Style Wireless Earbuds", "price": 2499, "old_price": 4999, "image": "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=400&h=400&fit=crop", "category": "Electronics", "badge": "Sale", "rating": 4.5, "is_featured": True, "description": "Premium wireless earbuds with active noise cancellation, 30-hour battery life and crystal clear sound."},
            {"name": "TWS Bluetooth Earbuds Deep Bass", "price": 1899, "old_price": 3499, "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop", "category": "Electronics", "badge": "Hot", "rating": 4.3, "is_featured": True, "description": "Deep bass wireless earbuds perfect for music lovers. Touch controls and long battery."},
            {"name": "Original Style White Earbuds", "price": 2199, "old_price": 3999, "image": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=400&h=400&fit=crop", "category": "Electronics", "badge": "Sale", "rating": 4.6, "is_featured": True, "description": "Classic white wireless earbuds with seamless connectivity and premium build."},
            {"name": "JBL Style Wireless Earbuds", "price": 2799, "old_price": 5499, "image": "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=400&h=400&fit=crop", "category": "Electronics", "badge": "New", "rating": 4.4, "is_featured": True, "description": "Powerful bass, water resistant design, perfect for workouts and daily use."},
            {"name": "3-in-1 Fast Charging Cable", "price": 599, "old_price": 1299, "image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400&h=400&fit=crop", "category": "Electronics", "badge": "Deal", "rating": 4.2, "is_featured": True, "description": "One cable for all devices. Lightning, Type-C and Micro USB. Fast charging support."},
            {"name": "Smart Watch Series 8 Style", "price": 3999, "old_price": 7999, "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop", "category": "Electronics", "badge": "Hot", "rating": 4.5, "description": "Full touch display, heart rate monitor, SpO2, multiple sports modes and 7-day battery."},
            {"name": "Wireless Bluetooth Speaker", "price": 2499, "old_price": 4499, "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop", "category": "Electronics", "badge": None, "rating": 4.3, "description": "Portable speaker with powerful sound, waterproof design and 12-hour playtime."},
            {"name": "Power Bank 20000mAh Fast Charge", "price": 1799, "old_price": 2999, "image": "https://images.unsplash.com/photo-1609091839311-bdfbff773ca1?w=400&h=400&fit=crop", "category": "Electronics", "badge": "Deal", "rating": 4.6, "description": "High capacity power bank with dual USB ports and fast charging technology."},

            # Fashion
            {"name": "Embroidered Lawn 3 Piece Unstitched", "price": 3499, "old_price": 5499, "image": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=400&fit=crop", "category": "Fashion", "badge": "Popular", "rating": 4.7, "description": "Premium quality embroidered lawn suit. Soft fabric, beautiful design. Perfect for summer."},
            {"name": "Premium Embroidered Kurti", "price": 1899, "old_price": 2999, "image": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=400&h=400&fit=crop", "category": "Fashion", "badge": None, "rating": 4.5, "description": "Elegant embroidered kurti for casual and formal wear. Comfortable and stylish."},
            {"name": "Luxury Formal Suit for Women", "price": 5999, "old_price": 8999, "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop", "category": "Fashion", "badge": "Premium", "rating": 4.8, "description": "Stunning formal wear with intricate embroidery. Ideal for weddings and special occasions."},
            {"name": "Printed Lawn Suit 3pc", "price": 2799, "old_price": 4199, "image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400&h=400&fit=crop", "category": "Fashion", "badge": "Sale", "rating": 4.4, "description": "Vibrant printed lawn 3-piece suit. Lightweight and perfect for daily wear."},
            {"name": "Chiffon Embroidered Dress", "price": 4499, "old_price": 6999, "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=400&h=400&fit=crop", "category": "Fashion", "badge": None, "rating": 4.6, "description": "Elegant chiffon dress with delicate embroidery. Graceful and comfortable."},
            {"name": "Silk Dupatta Embroidered", "price": 1599, "old_price": 2499, "image": "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=400&h=400&fit=crop", "category": "Fashion", "badge": None, "rating": 4.5, "description": "Premium silk dupatta with fine embroidery work. Adds elegance to any outfit."},

            # Beauty
            {"name": "NUDE Eyeshadow Palette", "price": 1499, "old_price": 2499, "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=400&fit=crop", "category": "Beauty", "badge": "Trending", "rating": 4.5, "description": "12 highly pigmented nude shades. Matte and shimmer finishes for everyday glam."},
            {"name": "Luxury Perfume Set for Her", "price": 2999, "old_price": 4999, "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=400&fit=crop", "category": "Beauty", "badge": "Hot", "rating": 4.7, "description": "Long-lasting fragrance set. Elegant notes of jasmine, vanilla and musk."},
            {"name": "Matte Lipstick Combo Pack (6 pcs)", "price": 899, "old_price": 1599, "image": "https://images.unsplash.com/photo-1586495777744-4413f21067fa?w=400&h=400&fit=crop", "category": "Beauty", "badge": "Deal", "rating": 4.3, "description": "Six beautiful matte shades. Non-drying formula with rich color payoff."},
            {"name": "Skincare Glow Kit Complete", "price": 2199, "old_price": 3499, "image": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&h=400&fit=crop", "category": "Beauty", "badge": None, "rating": 4.6, "description": "Complete skincare routine: cleanser, toner, serum and moisturizer for glowing skin."},

            # Home
            {"name": "Persian Style Carpet 5x7 ft", "price": 8999, "old_price": 14999, "image": "https://images.unsplash.com/photo-1600166898405-da9535204843?w=400&h=400&fit=crop", "category": "Home", "badge": "Best Seller", "rating": 4.8, "description": "Handcrafted Persian design carpet. Soft, durable and elegant for living rooms."},
            {"name": "Modern Geometric Rug", "price": 5499, "old_price": 8999, "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop", "category": "Home", "badge": None, "rating": 4.5, "description": "Contemporary geometric pattern rug. Soft underfoot and easy to clean."},
            {"name": "Luxury Velvet Cushion Set (4 pcs)", "price": 1999, "old_price": 3299, "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400&h=400&fit=crop", "category": "Home", "badge": "Sale", "rating": 4.4, "description": "Soft velvet cushions with elegant designs. Perfect for sofa and bed styling."},
            {"name": "Kitchen Knife Set Professional", "price": 1899, "old_price": 3299, "image": "https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400&h=400&fit=crop", "category": "Home", "badge": "Deal", "rating": 4.4, "description": "High-quality stainless steel knife set with wooden block. Sharp and durable."},

            # Men
            {"name": "Men's Embroidered Kurta", "price": 2499, "old_price": 3999, "image": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=400&fit=crop", "category": "Men", "badge": None, "rating": 4.5, "description": "Classic embroidered kurta for men. Comfortable cotton fabric, perfect for Eid and gatherings."},
            {"name": "Casual Cotton Shirt Men", "price": 1299, "old_price": 2199, "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=400&fit=crop", "category": "Men", "badge": "Sale", "rating": 4.2, "description": "Breathable cotton casual shirt. Smart look for office or weekend."},

            # Books
            {"name": "Deep Work - Cal Newport", "price": 799, "old_price": 1299, "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop", "category": "Books", "badge": "Bestseller", "rating": 4.9, "description": "Rules for focused success in a distracted world. A must-read for productivity."},
            {"name": "How to Start a Business", "price": 649, "old_price": 999, "image": "https://images.unsplash.com/photo-1589998059171-988d887df646?w=400&h=400&fit=crop", "category": "Books", "badge": None, "rating": 4.4, "description": "Practical guide to launching your own business with zero to minimal investment."},
            {"name": "Atomic Habits", "price": 899, "old_price": 1499, "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=400&fit=crop", "category": "Books", "badge": "Popular", "rating": 4.8, "description": "Tiny changes, remarkable results. The bestselling book on building good habits."},

            # Kids
            {"name": "Kids Fancy Party Dress", "price": 2199, "old_price": 3499, "image": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400&h=400&fit=crop", "category": "Kids", "badge": "New", "rating": 4.6, "description": "Beautiful party dress for little girls. Soft fabric, comfortable fit and adorable design."},

            # Accessories
            {"name": "Women's Handbag Premium", "price": 3499, "old_price": 5999, "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400&h=400&fit=crop", "category": "Accessories", "badge": "Luxury", "rating": 4.7, "description": "Premium quality handbag with elegant design. Spacious and stylish for daily use."},

            # Footwear
            {"name": "Sneakers Casual Unisex", "price": 2799, "old_price": 4499, "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop", "category": "Footwear", "badge": "Hot", "rating": 4.5, "description": "Comfortable casual sneakers for everyday wear. Lightweight and stylish design."},
        ]

        if Product.query.count() == 0:
            for p in products_data:
                cat_id = cat_map.get(p.pop("category"))
                product = Product(category_id=cat_id, **p)
                db.session.add(product)

        db.session.commit()
        print("✅ Database seeded successfully!")
if __name__ == '__main__':
    from app import app  # <-- Import ko yahan andar shift kar dein
    
    with app.app_context():
        existing_user = User.query.filter_by(email="mfareedsajjad@gmail.com").first()
        
        if not existing_user:
            new_user = User(
                email="mfareedsajjad@gmail.com",
                name="Fareed Sajjad",
                password=generate_password_hash("password123")
            )
            db.session.add(new_user)
            db.session.commit()
            print("✅ User added successfully!")
        else:
            print("⚠️ User already exists!")