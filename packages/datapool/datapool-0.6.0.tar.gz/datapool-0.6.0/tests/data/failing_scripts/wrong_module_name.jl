#
# Example Julia conversion script
#
# September  2, 2016 -- Andreas Scheidegger
# -------------------------------------------------------

# here the module name does not match the file name:

module wrong_function_name

using Dates
using DelimitedFiles


function convert(rawfile, outputfile)

    raw = DelimitedFiles.readdlm(rawfile, '\t', skipstart=2)

    # do some cleaning
    raw = raw[2:2:20,:]

    dat = [Dates.DateTime(str, "dd.mm.yyyy HH:MM") for str in raw[:,1]]

    # uncomment to simulate an error
    raw[100,100]

    # write file (Should be in standardizes file format. This is not the case here.)
    final = hcat(dat, raw[:,2])

    writedlm(outputfile, final, ';')
end

end
