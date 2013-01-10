deb:
	rm dist/*
	cd sl && dpkg-buildpackage -d -us -uc -F && cd .. && mv sl_* dist
iso:
	ubuntu-defaults-image --release precise --package dist/sl_*_all.deb --components main,restricted,universe
test:
	kvm -m 1024 -cdrom binary.hybrid.iso -boot d 

clean:
	rm dist/*

all:
	clean deb iso

.PHONY: deb iso test clean