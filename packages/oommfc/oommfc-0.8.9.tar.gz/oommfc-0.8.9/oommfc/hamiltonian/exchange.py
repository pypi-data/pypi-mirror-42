import micromagneticmodel as mm


class Exchange(mm.Exchange):
    @property
    def _script(self):
        mif = "# UniformExchange\n"
        mif += "Specify Oxs_UniformExchange {\n"
        mif += "  A {}\n".format(self.A)
        mif += "}\n\n"

        return mif
