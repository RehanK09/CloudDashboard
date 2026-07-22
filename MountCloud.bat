@echo off
cd /d D:\Apps\CloudDashboard

"D:\Apps\rclone\rclone.exe" mount GAurGhusMAurMhus: X: ^
--vfs-cache-mode full ^
--network-mode ^
--volname "Cloud Drive" ^
--rc ^
--rc-addr 127.0.0.1:5572 ^
--rc-no-auth ^
--log-level INFO

exit