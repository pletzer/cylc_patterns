module model_mod

    type :: input_t
        logical :: cold_start
        integer :: nsteps
        integer :: save_restart_steps
    end type

contains

    function parse_command_line_arguments(file_path) result(res)
        implicit none
        character(len=*) :: file_path
        integer :: res

        res = 0
        file_path = 'model.nml'
        if (command_argument_count() >= 1) then
            call get_command_argument(1, file_path)
        endif
        print *, 'file_path = ', file_path
    end function parse_command_line_arguments

    function read_namelist(file_path, input_data) result(res)
        implicit none

        character(len=*) :: file_path
        type(input_t) :: input_data
        integer :: ier, fu, res
        logical :: cold_start
        integer :: nsteps, save_restart_steps
        namelist /input/ cold_start, nsteps, save_restart_steps

        res = 0
        inquire(file=file_path, iostat=ier)
        if (ier /= 0) then
            res = 1
            return
        end if

        open(action='read', file=file_path, iostat=ier, newunit=fu)
        if (ier /= 0) then
            close(fu)
            res = 2
            return
        endif

        read(nml=input, iostat=ier, unit=fu)
        if (ier /= 0) then
            res = 3
            return
        endif

        close(fu)

        input_data%cold_start = cold_start
        input_data%nsteps = nsteps
        input_data%save_restart_steps = save_restart_steps
    end function read_namelist

    subroutine write_output(i)
            implicit none
            integer :: i, fu, ier
            character(len=32) :: file_name
            character(len=10) :: index_str

            write(index_str, '(I0)') i
            
            file_name = 'model_output_' // trim(index_str) // '.txt'
            print *, 'writing ', file_name
            open(action='write', file=file_name, iostat=ier, newunit=fu)
            close(fu)

    end subroutine write_output

end module model_mod

program model

    use model_mod

    implicit none
    integer :: ier
    character(len=256) :: file_path
    integer :: i
    type(input_t) :: input_data

    ier = parse_command_line_arguments(file_path)
    if (ier /= 0) error stop 'ERROR parsing command line arguments'

    ! read namelist
    ier = read_namelist(file_path, input_data)
    if (ier /= 0) error stop 'ERROR reading the namelist'


    ! loop
    do i = 1, input_data%nsteps
        call sleep(10) ! simulate number crunching

        if ( modulo(i, input_data%save_restart_steps) == 0) then
            call write_output(i)
        end if
    enddo


    stop 0 ! success


end program model