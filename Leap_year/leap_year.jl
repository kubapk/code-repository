function is_leap_year(year::Integer)
    if year % 100 == 0
        if year % 400 == 0
            return true
        elseif year % 4 == 0
            return false
        end 
    elseif year % 4 == 0
        return true
    else
        return false
    end
end 

println("Enter year: ")
year = parse(Int, readline())
println(is_leap_year(year))