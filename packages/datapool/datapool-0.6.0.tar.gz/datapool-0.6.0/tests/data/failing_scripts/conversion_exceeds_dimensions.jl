#
# Example Julia conversion script
#
# September  2, 2016 -- Andreas Scheidegger
# -------------------------------------------------------

module conversion_exceeds_dimensions

using DelimitedFiles
using Dates

function convert(rawfile, outputfile)

    raw = DelimitedFiles.readdlm(rawfile, '\t', skipstart=2)

    # do some cleaning
    raw = raw[2:2:20,1:5]

    dat = [Dates.DateTime(str, "dd.mm.yyyy HH:MM") for str in raw[:,1]]

    # uncomment to simulate an error
    raw[100,1]

    # write file (Should be in standardizes file format. This is not the case here.)
    final = hcat(dat, raw[:,2])

    writedlm(outputfile, final, ';')
end

end
