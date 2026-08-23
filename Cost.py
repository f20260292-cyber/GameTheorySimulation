class Latency:

    def __init__(self):
        pass

    def TotalCost(self, x):
        Ca = self.RouteA_Cost(x)
        return 100*( (x*Ca) + ((1-x)*4) )

    def RouteA_Cost(self, x):
        Ca = 2 + (2*x)
        if x > 0.7:
            Ca += 20 * ((x-0.7)**2)
        return Ca


if __name__ == "__main__":
    latency = Latency()
    for x in range(0, 100, 1):
        print(f"{x}  ->  {latency.TotalCost(x/100)}")