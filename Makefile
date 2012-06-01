deb:
	cd sl && dpkg-buildpackage -d -us -uc -F && cd .. && mv sl_* dist
iso:
	ubuntu-defaults-image --package dist/sl_*_all.deb --components main,restricted,universe
test:
	kvm -m 1024 -cdrom /home/dz0ny/sl/binary-hybrid.iso -vga std -sdl

clean:
	rm dist/*

all:
	clean deb iso

.PHONY: deb iso test clean