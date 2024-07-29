from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Konfigurasi koneksi ke MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="kasirsederhana"
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    return render_template('index.html', orders=orders)

@app.route('/submit', methods=['POST'])
def submit():
    nama = request.form['nama']
    nasi_goreng = int(request.form['nasiGoreng'])
    mie_goreng = int(request.form['mieGoreng'])
    sate_ayam = int(request.form['sateAyam'])
    teh_manis = int(request.form['tehManis'])
    kopi = int(request.form['kopi'])

    # Harga satuan
    harga_nasi_goreng = 15000
    harga_mie_goreng = 12000
    harga_sate_ayam = 20000
    harga_teh_manis = 5000
    harga_kopi = 8000

    # Hitung total harga
    total_harga = (nasi_goreng * harga_nasi_goreng +
                   mie_goreng * harga_mie_goreng +
                   sate_ayam * harga_sate_ayam +
                   teh_manis * harga_teh_manis +
                   kopi * harga_kopi)

    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO orders (nama, nasi_goreng, mie_goreng, sate_ayam, teh_manis, kopi, total_harga)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nama, nasi_goreng, mie_goreng, sate_ayam, teh_manis, kopi, total_harga))
    db.commit()
    cursor.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:order_id>')
def delete(order_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit(order_id):
    if request.method == 'POST':
        nama = request.form['nama']
        nasi_goreng = int(request.form['nasiGoreng'])
        mie_goreng = int(request.form['mieGoreng'])
        sate_ayam = int(request.form['sateAyam'])
        teh_manis = int(request.form['tehManis'])
        kopi = int(request.form['kopi'])

        harga_nasi_goreng = 15000
        harga_mie_goreng = 12000
        harga_sate_ayam = 20000
        harga_teh_manis = 5000
        harga_kopi = 8000

        total_harga = (nasi_goreng * harga_nasi_goreng +
                       mie_goreng * harga_mie_goreng +
                       sate_ayam * harga_sate_ayam +
                       teh_manis * harga_teh_manis +
                       kopi * harga_kopi)

        cursor = db.cursor()
        cursor.execute("""
            UPDATE orders 
            SET nama = %s, nasi_goreng = %s, mie_goreng = %s, sate_ayam = %s, teh_manis = %s, kopi = %s, total_harga = %s 
            WHERE id = %s
        """, (nama, nasi_goreng, mie_goreng, sate_ayam, teh_manis, kopi, total_harga, order_id))
        db.commit()
        cursor.close()
        return redirect(url_for('index'))
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    cursor.close()
    return render_template('edit.html', order=order)


if __name__ == '__main__':
    app.run(debug=True)
