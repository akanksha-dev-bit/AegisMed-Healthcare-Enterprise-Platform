"""
Rumah Sakit Anaverse — Landing Page Render Helper Functions.
Strictly implements the reference sections without duplicate navbars or emojis.
Uses native st.html(...) to avoid markdown parser whitespace/code block bugs.
Caches base64 hero image to prevent page lag and re-encoding on every rerun.
"""
import base64
from pathlib import Path
import streamlit as st


@st.cache_data(show_spinner=False)
def get_hero_image_src() -> str:
    """Return local hero.jpg as base64 data URI if present, cached across reruns."""
    hero_path = Path(__file__).resolve().parent / "assets" / "hero.jpg"
    if hero_path.exists() and hero_path.stat().st_size > 0:
        encoded = base64.b64encode(hero_path.read_bytes()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"
    return "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=900&q=80"


def render_hero():
    """Hero section: two columns (text left, doctor image right with straight floating badge)."""
    hero_src = get_hero_image_src()
    html = f"""
    <div style="padding: 2rem 0 3rem 0;">
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 3rem; align-items: center;">
        <div>
          <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; border-radius: 999px; background: #E8EDFF; color: #1E2FE0; font-size: 0.85rem; font-weight: 700; margin-bottom: 1.2rem; border: 1px solid rgba(30, 47, 224, 0.12);">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            </svg>
            Kesehatan Anda, Prioritas Kami
          </div>
          <h1 style="font-size: clamp(2.2rem, 4vw, 3.6rem); font-weight: 800; color: #0B1340; line-height: 1.15; letter-spacing: -0.025em; margin: 0 0 1.25rem 0;">
            Pelayanan Terbaik untuk <span style="color: #1E2FE0;">Kesehatan</span> Anda dan Keluarga
          </h1>
          <p style="font-size: 1.05rem; color: #6B7280; line-height: 1.7; margin: 0 0 2rem 0; max-width: 540px;">
            Kami hadir dengan layanan medis berkualitas, dokter berpengalaman, dan fasilitas modern untuk memberikan perawatan terbaik dengan kenyamanan maksimal.
          </p>
          <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
            <a href="#layanan" style="display: inline-flex; align-items: center; gap: 10px; padding: 12px 24px; border-radius: 12px; background: #1E2FE0; color: white; font-weight: 700; font-size: 0.95rem; text-decoration: none; box-shadow: 0 4px 14px rgba(30,47,224,0.3); white-space: nowrap;">
              Lihat Layanan
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
            <a href="#kontak" style="display: inline-flex; align-items: center; gap: 10px; padding: 12px 24px; border-radius: 12px; background: white; color: #1E2FE0; border: 1.5px solid #E5EAF5; font-weight: 700; font-size: 0.95rem; text-decoration: none; box-shadow: 0 2px 8px rgba(30,47,224,0.05); white-space: nowrap;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              Buat Janji Temu
            </a>
          </div>
        </div>
        <div style="position: relative; display: flex; justify-content: center;">
          <div style="width: 100%; max-width: 520px; height: 460px; border-radius: 28px; overflow: hidden; position: relative; box-shadow: 0 20px 50px rgba(11,19,64,0.12); border: 8px solid white;">
            <img src="{hero_src}" alt="Dokter Anak" style="width: 100%; height: 100%; object-fit: cover; object-position: center top;" />
            <div style="position: absolute; bottom: 18px; left: 18px; background: rgba(255, 255, 255, 0.94); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); padding: 12px 18px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.9); box-shadow: 0 10px 30px rgba(30,47,224,0.14); display: flex; align-items: center; gap: 12px;">
              <div style="width: 40px; height: 40px; border-radius: 10px; background: #E8EDFF; color: #1E2FE0; display: flex; align-items: center; justify-content: center;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>
              </div>
              <div>
                <div style="font-size: 0.9rem; font-weight: 800; color: #0B1340;">Akreditasi Paripurna</div>
                <div style="font-size: 0.75rem; color: #6B7280;">Standar Kementerian Kesehatan RI</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """
    st.html(html)


def render_stats():
    """Floating Stats Card: 4 columns with clean circular icons."""
    html = """
    <div style="background: white; border: 1px solid #E5EAF5; border-radius: 24px; padding: 28px 36px; box-shadow: 0 10px 40px rgba(30,47,224,0.08); margin: -1rem 0 3.5rem 0;">
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 24px;">
        <div style="display: flex; align-items: center; gap: 16px;">
          <div style="width: 52px; height: 52px; border-radius: 16px; background: #E8EDFF; color: #1E2FE0; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </div>
          <div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #0B1340; line-height: 1.1;">15+</div>
            <div style="font-size: 0.88rem; color: #6B7280; font-weight: 500;">Dokter Spesialis</div>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 16px;">
          <div style="width: 52px; height: 52px; border-radius: 16px; background: #E8EDFF; color: #1E2FE0; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="22" y1="11" x2="16" y2="11"/></svg>
          </div>
          <div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #0B1340; line-height: 1.1;">25.000+</div>
            <div style="font-size: 0.88rem; color: #6B7280; font-weight: 500;">Pasien Terlayani</div>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 16px;">
          <div style="width: 52px; height: 52px; border-radius: 16px; background: #E8EDFF; color: #1E2FE0; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 7v11a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V7"/><path d="M21 7l-9 5-9-5"/><path d="M2 3h20v4H2z"/></svg>
          </div>
          <div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #0B1340; line-height: 1.1;">120+</div>
            <div style="font-size: 0.88rem; color: #6B7280; font-weight: 500;">Kamar Perawatan</div>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 16px;">
          <div style="width: 52px; height: 52px; border-radius: 16px; background: #E8EDFF; color: #1E2FE0; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          </div>
          <div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #0B1340; line-height: 1.1;">98%</div>
            <div style="font-size: 0.88rem; color: #6B7280; font-weight: 500;">Kepuasan Pasien</div>
          </div>
        </div>
      </div>
    </div>
    """
    st.html(html)


def render_about():
    """About Section: hospital building image left, description & 4 feature tiles right."""
    html = """
    <div id="tentang" style="padding: 2.5rem 0 3.5rem 0;">
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 3.5rem; align-items: center;">
        <div style="border-radius: 28px; overflow: hidden; height: 420px; box-shadow: 0 16px 45px rgba(11,19,64,0.08); border: 1px solid #E5EAF5;">
          <img src="https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?auto=format&fit=crop&w=900&q=80" alt="Gedung Rumah Sakit" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
        <div style="position: relative;">
          <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; border-radius: 999px; background: #E8EDFF; color: #1E2FE0; font-size: 0.85rem; font-weight: 700; margin-bottom: 1rem; border: 1px solid rgba(30, 47, 224, 0.12);">
            Tentang Kami
          </div>
          <h2 style="font-size: 2.2rem; font-weight: 800; color: #0B1340; line-height: 1.25; margin: 0 0 1rem 0; letter-spacing: -0.02em;">
            Rumah Sakit <span style="color: #1E2FE0;">Anaverse</span> Untuk Hidup yang Lebih Sehat
          </h2>
          <p style="font-size: 1rem; color: #6B7280; line-height: 1.7; margin: 0 0 1.8rem 0;">
            Didirikan dengan komitmen tinggi terhadap keselamatan pasien, kami menggabungkan keahlian klinis dokter spesialis dengan peralatan mutakhir untuk memberikan perawatan yang komprehensif, humanis, dan tepercaya.
          </p>
          <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            <div style="background: white; border: 1px solid #E5EAF5; border-radius: 16px; padding: 14px 18px; display: flex; align-items: center; gap: 14px; box-shadow: 0 2px 8px rgba(30,47,224,0.04);">
              <div style="width: 42px; height: 42px; border-radius: 12px; background: #E8EDFF; color: #1E2FE0; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              </div>
              <div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #0B1340;">Pelayanan 24 Jam</div>
                <div style="font-size: 0.75rem; color: #6B7280;">Siap siaga setiap saat</div>
              </div>
            </div>
            <div style="background: white; border: 1px solid #E5EAF5; border-radius: 16px; padding: 14px 18px; display: flex; align-items: center; gap: 14px; box-shadow: 0 2px 8px rgba(30,47,224,0.04);">
              <div style="width: 42px; height: 42px; border-radius: 12px; background: #E8EDFF; color: #1E2FE0; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              </div>
              <div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #0B1340;">Tenaga Profesional</div>
                <div style="font-size: 0.75rem; color: #6B7280;">Dokter bersertifikasi</div>
              </div>
            </div>
            <div style="background: white; border: 1px solid #E5EAF5; border-radius: 16px; padding: 14px 18px; display: flex; align-items: center; gap: 14px; box-shadow: 0 2px 8px rgba(30,47,224,0.04);">
              <div style="width: 42px; height: 42px; border-radius: 12px; background: #E8EDFF; color: #1E2FE0; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
              </div>
              <div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #0B1340;">Fasilitas Modern</div>
                <div style="font-size: 0.75rem; color: #6B7280;">Teknologi diagnostik terkini</div>
              </div>
            </div>
            <div style="background: white; border: 1px solid #E5EAF5; border-radius: 16px; padding: 14px 18px; display: flex; align-items: center; gap: 14px; box-shadow: 0 2px 8px rgba(30,47,224,0.04);">
              <div style="width: 42px; height: 42px; border-radius: 12px; background: #E8EDFF; color: #1E2FE0; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              </div>
              <div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #0B1340;">Perawatan Berkualitas</div>
                <div style="font-size: 0.75rem; color: #6B7280;">Standar internasional</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """
    st.html(html)


def render_services():
    """Layanan Kami: 6 image cards in a clean rounded container."""
    services = [
        ("Poli Spesialis", "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=400&q=80"),
        ("Rawat Inap", "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=400&q=80"),
        ("IGD 24 Jam", "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=400&q=80"),
        ("Radiologi", "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=400&q=80"),
        ("Laboratorium", "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=400&q=80"),
        ("Farmasi 24 Jam", "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=400&q=80"),
    ]
    cards_html = "".join([
        f"""
        <div style="background: #FAFCFF; border: 1px solid #E5EAF5; border-radius: 18px; padding: 10px; text-align: center; transition: all 0.25s ease;">
          <div style="width: 100%; height: 120px; border-radius: 14px; overflow: hidden; margin-bottom: 12px;">
            <img src="{img}" alt="{name}" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>
          <div style="font-size: 0.92rem; font-weight: 700; color: #0B1340; padding: 4px 6px 8px 6px;">{name}</div>
        </div>
        """ for name, img in services
    ])

    html = f"""
    <div id="layanan" style="padding: 2.5rem 0 3.5rem 0;">
      <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.8rem;">
        <div>
          <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; border-radius: 999px; background: #E8EDFF; color: #1E2FE0; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.6rem; border: 1px solid rgba(30, 47, 224, 0.12);">
            Layanan Kami
          </div>
          <h2 style="font-size: 2.1rem; font-weight: 800; color: #0B1340; margin: 0; letter-spacing: -0.02em;">
            Layanan Medis <span style="color: #1E2FE0;">Komprehensif</span>
          </h2>
        </div>
        <div style="font-size: 0.95rem; font-weight: 700; color: #1E2FE0;">Lihat Semua Layanan &rarr;</div>
      </div>
      <div style="background: white; border: 1px solid #E5EAF5; border-radius: 24px; padding: 28px; box-shadow: 0 10px 40px rgba(30,47,224,0.06);">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 18px;">
          {cards_html}
        </div>
      </div>
    </div>
    """
    st.html(html)


def render_doctors():
    """Dokter Kami: left introduction, right 4 doctor cards with star ratings."""
    doctors = [
        ("dr. Andika Pratama", "Spesialis Jantung", "4.9", "https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&w=500&q=80"),
        ("dr. Salsabila Putri", "Spesialis Anak", "4.9", "https://images.unsplash.com/photo-1594824813511-30c1154564c7?auto=format&fit=crop&w=500&q=80"),
        ("dr. Budi Santoso", "Spesialis Bedah", "4.8", "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&w=500&q=80"),
        ("dr. Meilani Putri", "Spesialis Penyakit Dalam", "4.9", "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&w=500&q=80"),
    ]
    docs_html = "".join([
        f"""
        <div style="background: white; border: 1px solid #E5EAF5; border-radius: 20px; overflow: hidden; box-shadow: 0 6px 20px rgba(30,47,224,0.05);">
          <div style="width: 100%; height: 210px; overflow: hidden; position: relative; background: #E8EDFF;">
            <img src="{img}" alt="{name}" style="width: 100%; height: 100%; object-fit: cover; object-position: top center;" />
            <div style="position: absolute; top: 12px; right: 12px; background: rgba(255,255,255,0.92); backdrop-filter: blur(8px); padding: 3px 10px; border-radius: 999px; font-size: 0.8rem; font-weight: 800; color: #0B1340; box-shadow: 0 2px 8px rgba(0,0,0,0.06); display: flex; align-items: center; gap: 4px;">
              <span style="color: #F5B301;">★</span> {rating}
            </div>
          </div>
          <div style="padding: 16px 18px;">
            <div style="font-size: 1rem; font-weight: 800; color: #0B1340; margin-bottom: 3px;">{name}</div>
            <div style="font-size: 0.82rem; font-weight: 600; color: #1E2FE0;">{spec}</div>
          </div>
        </div>
        """ for name, spec, rating, img in doctors
    ])

    html = f"""
    <div id="dokter" style="padding: 2.5rem 0 3.5rem 0;">
      <div style="display: grid; grid-template-columns: 320px 1fr; gap: 3rem; align-items: center;">
        <div>
          <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; border-radius: 999px; background: #E8EDFF; color: #1E2FE0; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.8rem; border: 1px solid rgba(30, 47, 224, 0.12);">
            Dokter Kami
          </div>
          <h2 style="font-size: 2.1rem; font-weight: 800; color: #0B1340; line-height: 1.25; margin: 0 0 1rem 0; letter-spacing: -0.02em;">
            Dokter Spesialis <span style="color: #1E2FE0;">Berpengalaman</span>
          </h2>
          <p style="font-size: 0.95rem; color: #6B7280; line-height: 1.7; margin: 0 0 1.8rem 0;">
            Ditangani oleh tim dokter spesialis terkemuka dengan keahlian komprehensif dan empati tinggi terhadap proses pemulihan pasien.
          </p>
          <a href="#kontak" style="display: inline-flex; align-items: center; gap: 8px; padding: 12px 22px; border-radius: 12px; background: #1E2FE0; color: white; font-weight: 700; font-size: 0.92rem; text-decoration: none;">
            Lihat Semua Dokter
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </a>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 18px;">
          {docs_html}
        </div>
      </div>
    </div>
    """
    st.html(html)


def render_facilities():
    """Fasilitas Modern (Dark Navy Section): 5 glass-bordered image tiles."""
    facilities = [
        ("Ruang ICU", "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=300&q=80"),
        ("Kamar VIP", "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=300&q=80"),
        ("Ruang Operasi", "https://images.unsplash.com/photo-1551076805-e1869033e561?auto=format&fit=crop&w=300&q=80"),
        ("Laboratorium", "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=300&q=80"),
        ("Ambulans 24 Jam", "https://images.unsplash.com/photo-1587745416684-47953f16f02f?auto=format&fit=crop&w=300&q=80"),
    ]
    tiles_html = "".join([
        f"""
        <div style="background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.16); border-radius: 16px; overflow: hidden; text-align: center;">
          <div style="width: 100%; height: 100px; overflow: hidden;">
            <img src="{img}" alt="{name}" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>
          <div style="font-size: 0.82rem; font-weight: 700; color: white; padding: 10px 8px;">{name}</div>
        </div>
        """ for name, img in facilities
    ])

    html = f"""
    <div id="fasilitas" style="background: linear-gradient(135deg, #0B1340 0%, #0d174d 60%, #15226e 100%); border-radius: 28px; padding: 52px 48px; margin: 3rem 0; color: white; box-shadow: 0 20px 50px rgba(11,19,64,0.2);">
      <div style="display: grid; grid-template-columns: 320px 1fr; gap: 3rem; align-items: center;">
        <div>
          <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; border-radius: 999px; background: rgba(255,255,255,0.12); color: white; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.8rem; border: 1px solid rgba(255,255,255,0.2);">
            Fasilitas Modern
          </div>
          <h2 style="font-size: 2.1rem; font-weight: 800; color: white; line-height: 1.25; margin: 0 0 1rem 0; letter-spacing: -0.02em;">
            Fasilitas Modern untuk Perawatan Terbaik
          </h2>
          <p style="font-size: 0.95rem; color: rgba(255,255,255,0.78); line-height: 1.7; margin: 0;">
            Didesain khusus untuk memenuhi standar sterilitas internasional serta memberikan kenyamanan optimal bagi pasien dan keluarga.
          </p>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 14px;">
          {tiles_html}
        </div>
      </div>
    </div>
    """
    st.html(html)


def render_news():
    """Berita & Tips Kesehatan: 4 clean article cards."""
    articles = [
        ("Kesehatan Jantung", "#DC2626", "#FEE2E2", "5 Pola Makan Sehat untuk Mencegah Risiko Jantung Koroner", "03 November 2026 · 4 menit baca", "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=500&q=80"),
        ("Kesehatan Anak", "#D97706", "#FEF3C7", "Pentingnya Imunisasi Dasar Lengkap untuk Tumbuh Kembang Buah Hati", "01 November 2026 · 3 menit baca", "https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=500&q=80"),
        ("Gaya Hidup", "#16A34A", "#DCFCE7", "Menjaga Keseimbangan Mental & Fisik di Tengah Kesibukan Modern", "28 Oktober 2026 · 5 menit baca", "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=500&q=80"),
        ("Kesehatan Lansia", "#4338CA", "#E0E7FF", "Tips Menjaga Kepadatan Tulang dan Sendi Aktif di Usia Emas", "25 Oktober 2026 · 4 menit baca", "https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?auto=format&fit=crop&w=500&q=80"),
    ]
    news_html = "".join([
        f"""
        <div style="background: white; border: 1px solid #E5EAF5; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 16px rgba(30,47,224,0.04);">
          <div style="width: 100%; height: 160px; overflow: hidden;">
            <img src="{img}" alt="{title}" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>
          <div style="padding: 18px;">
            <span style="display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 0.72rem; font-weight: 700; color: {tag_color}; background: {tag_bg}; margin-bottom: 10px;">{tag}</span>
            <div style="font-size: 0.98rem; font-weight: 800; color: #0B1340; line-height: 1.35; margin-bottom: 8px;">{title}</div>
            <div style="font-size: 0.78rem; color: #6B7280;">{date}</div>
          </div>
        </div>
        """ for tag, tag_color, tag_bg, title, date, img in articles
    ])

    html = f"""
    <div id="berita" style="padding: 2.5rem 0 3.5rem 0;">
      <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.8rem;">
        <div>
          <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; border-radius: 999px; background: #E8EDFF; color: #1E2FE0; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.6rem; border: 1px solid rgba(30, 47, 224, 0.12);">
            Artikel Terkini
          </div>
          <h2 style="font-size: 2.1rem; font-weight: 800; color: #0B1340; margin: 0; letter-spacing: -0.02em;">
            Berita & Tips <span style="color: #1E2FE0;">Kesehatan</span>
          </h2>
        </div>
        <div style="font-size: 0.95rem; font-weight: 700; color: #1E2FE0;">Lihat Semua Berita &rarr;</div>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px;">
        {news_html}
      </div>
    </div>
    """
    st.html(html)


def render_cta():
    """CTA Banner: urgent medical assistance, hotline phone, action card."""
    html = """
    <div id="kontak" style="background: linear-gradient(135deg, #1E2FE0 0%, #2035F0 50%, #0F1B8C 100%); border-radius: 28px; padding: 48px 56px; color: white; box-shadow: 0 20px 50px rgba(30,47,224,0.3); margin: 3rem 0;">
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 3rem; align-items: center;">
        <div>
          <h2 style="font-size: 2.2rem; font-weight: 800; line-height: 1.25; margin: 0 0 1rem 0; color: white;">
            Butuh Bantuan Medis Segera?
          </h2>
          <p style="font-size: 1rem; opacity: 0.9; line-height: 1.6; margin: 0 0 1.5rem 0;">
            Kami siap melayani Anda 24 jam sehari, 7 hari seminggu. Tanggap darurat cepat dengan armada ambulans siaga dan dokter jaga profesional.
          </p>
          <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.18); padding: 6px 14px; border-radius: 999px; font-size: 0.82rem; font-weight: 700;">IGD 24 Jam</div>
            <div style="background: rgba(255,255,255,0.18); padding: 6px 14px; border-radius: 999px; font-size: 0.82rem; font-weight: 700;">Tenaga Medis Profesional</div>
            <div style="background: rgba(255,255,255,0.18); padding: 6px 14px; border-radius: 999px; font-size: 0.82rem; font-weight: 700;">Fasilitas Lengkap</div>
          </div>
        </div>
        <div style="background: white; border-radius: 22px; padding: 32px; color: #0B1340; box-shadow: 0 14px 40px rgba(0,0,0,0.18); text-align: center;">
          <div style="font-size: 0.82rem; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em;">Hotline Gawat Darurat</div>
          <div style="font-size: 1.7rem; font-weight: 800; color: #1E2FE0; margin: 8px 0 4px 0; display: flex; align-items: center; justify-content: center; gap: 8px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            (021) 1234 5678
          </div>
          <p style="font-size: 0.82rem; color: #6B7280; margin: 0 0 18px 0;">Atau Jadwalkan Konsultasi Dokter Spesialis</p>
          <div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; width: 100%; padding: 12px; border-radius: 12px; background: #1E2FE0; color: white; font-weight: 700; font-size: 0.92rem;">
            Jadwalkan Konsultasi
          </div>
        </div>
      </div>
    </div>
    """
    st.html(html)


def render_landing_page():
    """Render the full landing page in order."""
    render_hero()
    render_stats()
    render_about()
    render_services()
    render_doctors()
    render_facilities()
    render_news()
    render_cta()
