function Matriz = rotacionaMatriz(eixoRotacao, q)
    //função que rotaciona nos respectivos eixos
    select eixoRotacao
        case 'x'
            Matriz = [1 0 0 0; 0 cosd(q) -sind(q) 0; 0 sind(q) cosd(q) 0; 0 0 0 1];
        case 'y'
            Matriz = [cosd(q) 0 sind(q) 0; 0 1 0 0; -sind(q) 0 cosd(q) 0; 0 0 0 1];
        case 'z'
            Matriz = [cosd(q) -sind(q) 0 0; sind(q) cosd(q) 0 0; 0 0 1 0; 0 0 0 1];
     end
endfunction
