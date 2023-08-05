/*-----------------------------------------------------------------------------
| Copyright (c) 2014-2018, Nucleic
|
| Distributed under the terms of the BSD 3-Clause License.
|
| The full license is in the file LICENSE, distributed with this software.
|----------------------------------------------------------------------------*/
#pragma once

#include <Python.h>


namespace atom
{

// POD struct - all member fields are considered private
struct TypedContainerList
{
	PyListObject list;
	Member* validator;
    CAtomPointer* pointer;
    Member* member;

	static PyTypeObject TypeObject;

	static bool Ready();

	static bool TypeCheck( PyObject* ob )
	{
		return PyObject_TypeCheck( ob, &TypeObject ) != 0;
	}
};

PyObject*
AtomCList_New( Py_ssize_t size, CAtom* atom, Member* validator, Member* member );

} // namespace atom
