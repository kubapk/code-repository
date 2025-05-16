#=
________________________________________________________________________

Cálculo del coeficiente B_3 del virial mediante integración Monte Carlo
________________________________________________________________________

@author Kuba Kane
Creado 17 de abril 2025
=#
using Random
Random.seed!(1232)

SIGMA = 1
N = 10^5
pi = acos(-1)
B_3 = 5*pi^2/18
println("**", B_3)


function calcular_valor_absoluto(vector)
    x_coord = vector[1]
    y_coord = vector[2]
    z_coord = vector[3]
    
    return sqrt(x_coord^2 + y_coord^2 + z_coord^2)
end 


function comparar_posiciones(posicion_2, posicion_3, sigma)
    diferencia_en_posiciones = posicion_2 - posicion_3
    diferencia_absoluto = calcular_valor_absoluto(diferencia_en_posiciones)

    if diferencia_absoluto < sigma
        return true
    else
        return false
    end
end


function calcular_suma(sigma, no_puntos)
    SUMA = 0

    for i in 1:no_puntos
        t_max = 1/3 * sigma^3
        phi_max = 2*pi

        #generación del punto 2
        t = t_max*rand()
        w = 2*rand() - 1
        phi = phi_max*rand()

        r = (3t)^(1/3)
        theta = acos(w)

        x = r*sin(theta)*cos(phi)
        y = r*sin(theta)*sin(phi)
        z = r*cos(theta)

        punto_2 = [x, y, z]

        #generación del punto 3
        t = t_max*rand()
        w = 2*rand() - 1
        phi = phi_max*rand()

        r = (3t)^(1/3)
        theta = acos(w)

        x = r*sin(theta)*cos(phi)
        y = r*sin(theta)*sin(phi)
        z = r*cos(theta)

        punto_3 = [x, y, z]

        diferencia_menos_sigma = comparar_posiciones(punto_2, punto_3, sigma)

        if diferencia_menos_sigma == true
            SUMA = SUMA + 1
        end 

        #=
        println("Quieres que sale cada iteración en la terminal? [Y/N]")
        display = readline()
        if display == "Y"
            println(" ")
            println("Iteracion ", i)
            println("Coordenadas de esferas 2 y 3: (2)", punto_2, " (3)", punto_3)
            println("Diferencia entre esferas 2 y 3 es menor que sigma? ", diferencia_menos_sigma)
        end 
        =#
    end
    return SUMA*((4*pi/3)*sigma^3)^2 /(3*N)
end


function calcular_cambio_porcental(no_1, no_2)
    diferencia = no_1 - no_2
    diferencia_porcentual = (diferencia/no_1)*100
    return round.(diferencia_porcentual; sigdigits=5)
end


suma_total = calcular_suma(SIGMA, N)
println("La suma final es ", suma_total)

porcentaje = calcular_cambio_porcental(B_3, suma_total)
println("Este valor tiene un acuerdo de ", porcentaje, "% con el valor exacto de B_3, habiendo generado ", N," puntos.")