-- Semua anak Budi
-- select nama,kelamin from keluarga where anakdari=1 

-- Semua Cucu Budi
-- SELECT cucu.nama,cucu.kelamin FROM 
-- keluarga kakek 
-- JOIN keluarga ortu ON ortu.anakdari = kakek.id 
-- JOIN keluarga cucu ON cucu.anakdari=ortu.id 

-- Semua Cucu Perempuan Budi
-- SELECT cucu.nama,cucu.kelamin FROM 
-- keluarga kakek 
-- JOIN keluarga ortu ON ortu.anakdari = kakek.id 
-- JOIN keluarga cucu ON cucu.anakdari=ortu.id where cucu.kelamin="Perempuan" 

-- Bibi dari Fara
-- select distinct b.nama,b.kelamin 
-- from keluarga kk 
-- JOIN keluarga a ON a.id=kk.anakdari
-- Join keluarga b ON b.anakdari=a.anakdari where b.id!=(select anakdari from keluarga where nama="Farah") and b.kelamin="Perempuan"

-- Sepupu laki-laki Hani
-- select distinct c.nama,c.kelamin
-- from keluarga kk 
-- JOIN keluarga a ON a.id=kk.anakdari
-- Join keluarga b ON b.anakdari=a.anakdari
-- join keluarga c ON c.anakdari=b.id where b.id!=(select anakdari from keluarga where nama="Hani") and c.kelamin="Laki-laki"
