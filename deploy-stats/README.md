# Patches Per Deployment

How many patches make up a WMF deployment?

```
for i in {1..25}; do
    python3 deploy-stats-historic.py -w "1.3x.0-wmf.${i}" | tee patches-for-1.3x.tsv
done
```

Then I plotted using gnuplot:

```
set boxwidth 0.5
set style fill solid
plot 'patches-for-1.3x.tsv' using 2: xtic(1) with lines
```

# The graphs

## 1.31

![1.31.png](1.31.png)

## 1.32

![1.32.png](1.32.png)

## 1.33

![1.33.png](1.33.png)

## 1.34

![1.34.png](1.34.png)

## 1.35

![1.35.png](1.35.png)

## 1.31 -- 1.35

![1.31-1.35.png](1.31-1.35.png)
