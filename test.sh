for file in Tests/*; do
  python Tests/${file##*/}
done