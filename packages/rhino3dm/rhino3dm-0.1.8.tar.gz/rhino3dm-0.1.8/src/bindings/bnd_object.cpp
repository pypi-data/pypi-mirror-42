#include "bindings.h"
#include "base64.h"

BND_CommonObject::BND_CommonObject()
{
}

BND_CommonObject::~BND_CommonObject()
{
  // m_component_ref should almost always track the lifetime of the ON_Object
  if (m_object && m_component_ref.IsEmpty())
    delete m_object;
}

BND_CommonObject::BND_CommonObject(ON_Object* obj, const ON_ModelComponentReference* compref)
{
  SetTrackedPointer(obj, compref);
}

void BND_CommonObject::SetTrackedPointer(ON_Object* obj, const ON_ModelComponentReference* compref)
{
  if( compref )
  {
    m_component_ref = *compref;
  }
  else
  {
    ON_ModelComponent* model_component = ON_ModelComponent::Cast(obj);
    if (model_component)
      m_component_ref = ON_ModelComponentReference::CreateForExperts(model_component, true);
  }
  m_object = obj;
}

BND_CommonObject* BND_CommonObject::CreateWrapper(ON_Object* obj, const ON_ModelComponentReference* compref)
{
  if( nullptr == obj )
    return nullptr;

  ON_Geometry* geometry = ON_Geometry::Cast(obj);
  if( geometry )
  {
    ON_Mesh* mesh = ON_Mesh::Cast(obj);
    if( mesh )
      return new BND_Mesh(mesh, compref);
    ON_Brep* brep = ON_Brep::Cast(obj);
    if( brep )
      return new BND_Brep(brep, compref);
    ON_Curve* curve = ON_Curve::Cast(obj);
    if(curve)
    {
      ON_NurbsCurve* nc = ON_NurbsCurve::Cast(obj);
      if( nc )
        return new BND_NurbsCurve(nc, compref);
      ON_LineCurve* lc = ON_LineCurve::Cast(obj);
      if( lc )
        return new BND_LineCurve(lc, compref);
      ON_PolylineCurve* plc = ON_PolylineCurve::Cast(obj);
      if( plc )
        return new BND_PolylineCurve(plc, compref);
      ON_PolyCurve* pc = ON_PolyCurve::Cast(obj);
      if( pc )
        return new BND_PolyCurve(pc, compref);
      ON_ArcCurve* ac = ON_ArcCurve::Cast(obj);
      if (ac)
        return new BND_ArcCurve(ac, compref);
      ON_CurveProxy* proxy = ON_CurveProxy::Cast(obj);
      if (proxy)
        return new BND_CurveProxy(proxy, compref);
      return new BND_Curve(curve, compref);
    }

    ON_Surface* surface = ON_Surface::Cast(obj);
    if (surface)
    {
      ON_NurbsSurface* ns = ON_NurbsSurface::Cast(obj);
      if (ns)
        return new BND_NurbsSurface(ns, compref);
      ON_Extrusion* extr = ON_Extrusion::Cast(obj);
      if (extr)
        return new BND_Extrusion(extr, compref);
      ON_SurfaceProxy* proxy = ON_SurfaceProxy::Cast(obj);
      if (proxy)
      {
        ON_BrepFace* brepface = ON_BrepFace::Cast(obj);
        if (brepface)
          return new BND_BrepFace(brepface, compref);
        return new BND_SurfaceProxy(proxy, compref);
      }
      ON_RevSurface* revsrf = ON_RevSurface::Cast(obj);
      if (revsrf)
        return new BND_RevSurface(revsrf, compref);
      return new BND_Surface(surface, compref);
    }

    ON_Point* point = ON_Point::Cast(obj);
    if (point)
      return new BND_Point(point, compref);

    ON_PointCloud* pointcloud = ON_PointCloud::Cast(obj);
    if (pointcloud)
      return new BND_PointCloud(pointcloud, compref);

    ON_PointGrid* pointgrid = ON_PointGrid::Cast(obj);
    if (pointgrid)
      return new BND_PointGrid(pointgrid, compref);

    ON_Viewport* viewport = ON_Viewport::Cast(obj);
    if( viewport )
      return new BND_Viewport(viewport, compref);

    ON_Hatch* hatch = ON_Hatch::Cast(obj);
    if (hatch)
      return new BND_Hatch(hatch, compref);

    ON_InstanceRef* iref = ON_InstanceRef::Cast(obj);
    if (iref)
      return new BND_InstanceReferenceGeometry(iref, compref);

    return new BND_GeometryBase(geometry, compref);
  }

  ON_Material* material = ON_Material::Cast(obj);
  if (material)
    return new BND_Material(material, compref);

  ON_Layer* layer = ON_Layer::Cast(obj);
  if (layer)
    return new BND_Layer(layer, compref);

  ON_Texture* texture = ON_Texture::Cast(obj);
  if (texture)
    return new BND_Texture(texture, compref);

  ON_Bitmap* bitmap = ON_Bitmap::Cast(obj);
  if (bitmap)
    return new BND_Bitmap(bitmap, compref);

  ON_TextureMapping* texturemapping = ON_TextureMapping::Cast(obj);
  if (texturemapping)
    return new BND_TextureMapping(texturemapping, compref);

  ON_DimStyle* dimstyle = ON_DimStyle::Cast(obj);
  if (dimstyle)
    return new BND_DimensionStyle(dimstyle, compref);

  ON_InstanceDefinition* idef = ON_InstanceDefinition::Cast(obj);
  if (idef)
    return new BND_InstanceDefinitionGeometry(idef, compref);

  return new BND_CommonObject(obj, compref);
}

BND_CommonObject* BND_CommonObject::CreateWrapper(const ON_ModelComponentReference& compref)
{
  const ON_ModelComponent* model_component = compref.ModelComponent();
  const ON_ModelGeometryComponent* geometryComponent = ON_ModelGeometryComponent::Cast(model_component);
  if (nullptr == geometryComponent)
    return nullptr;

  ON_Object* obj = const_cast<ON_Geometry*>(geometryComponent->Geometry(nullptr));
  return CreateWrapper(obj, &compref);
}


RH_C_FUNCTION ON_Write3dmBufferArchive* ON_WriteBufferArchive_NewWriter(const ON_Object* pConstObject, int rhinoversion, bool writeuserdata, unsigned int* length)
{
  ON_Write3dmBufferArchive* rc = nullptr;

  if( pConstObject && length )
  {
    ON_UserDataHolder holder;
    if( !writeuserdata )
      holder.MoveUserDataFrom(*pConstObject);
    *length = 0;
    size_t sz = pConstObject->SizeOf() + 512; // 256 was too small on x86 builds to account for extra data written

    // figure out the appropriate version number
    unsigned int on_version__to_write = ON_BinaryArchive::ArchiveOpenNURBSVersionToWrite(rhinoversion, ON::Version());

    rc = new ON_Write3dmBufferArchive(sz, 0, rhinoversion, on_version__to_write);
    if( rc->WriteObject(pConstObject) )
    {
      *length = (unsigned int)rc->SizeOfArchive();
    }
    else
    {
      delete rc;
      rc = nullptr;
    }
    if( !writeuserdata )
      holder.MoveUserDataTo(*pConstObject, false);
  }
  return rc;
}

#if defined(__EMSCRIPTEN__)
emscripten::val BND_CommonObject::Encode() const
{
  emscripten::val v(emscripten::val::object());
  v.set("version", emscripten::val(10000));
  const int rhinoversion = 60;
  v.set("archive3dm", emscripten::val(rhinoversion));
  unsigned int on_version__to_write = ON_BinaryArchive::ArchiveOpenNURBSVersionToWrite(rhinoversion, ON::Version());
  v.set("opennurbs", emscripten::val((int)on_version__to_write));

  unsigned int length=0;
  ON_Write3dmBufferArchive* archive = ON_WriteBufferArchive_NewWriter(m_object, 60, true, &length);
  std::string data = "";
  if( length>0 && archive )
  {
    unsigned char* buffer = (unsigned char*)archive->Buffer();
    data = base64_encode(buffer, length);
  }
  if( archive )
    delete archive;

  v.set("data", emscripten::val(data));
  return v;
}

emscripten::val BND_CommonObject::toJSON(emscripten::val key)
{
  return Encode();
}

#endif
#if defined(ON_PYTHON_COMPILE)

static void SetupEncodedDictionaryVersions(pybind11::dict& d, int& rhinoversion)
{
  d["version"] = 10000;
  rhinoversion = 60;
  d["archive3dm"] = rhinoversion;
  unsigned int on_version__to_write = ON_BinaryArchive::ArchiveOpenNURBSVersionToWrite(rhinoversion, ON::Version());
  d["opennurbs"] = (int)(on_version__to_write);
}

pybind11::dict BND_CommonObject::Encode() const
{
  pybind11::dict d;
  int rhinoversion;
  SetupEncodedDictionaryVersions(d, rhinoversion);
  unsigned int length=0;
  ON_Write3dmBufferArchive* archive = ON_WriteBufferArchive_NewWriter(m_object, rhinoversion, true, &length);
  std::string data = "";
  if( length>0 && archive )
  {
    unsigned char* buffer = (unsigned char*)archive->Buffer();
    data = base64_encode(buffer, length);
  }
  if( archive )
    delete archive;

  d["data"] = data;
  return d;
}

RH_C_FUNCTION ON_Write3dmBufferArchive* ON_WriteBufferArchive_NewMemoryWriter(int rhinoversion)
{
  // figure out the appropriate version number
  unsigned int on_version__to_write = ON_BinaryArchive::ArchiveOpenNURBSVersionToWrite(rhinoversion, ON::Version());

  ON_Write3dmBufferArchive* rc = new ON_Write3dmBufferArchive(0, 0, rhinoversion, on_version__to_write);
  return rc;
}

static ON_UUID RhinoDotNetDictionaryId()
{
  // The .NET dictionary Id we have been using for a long time
  //21EE7933-1E2D-4047-869E-6BDBF986EA11
  static const GUID id =
  { 0x21ee7933, 0x1e2d, 0x4047, { 0x86, 0x9e, 0x6b, 0xdb, 0xf9, 0x86, 0xea, 0x11 } };
  return id;
}

enum class ItemType : int
{
  // values <= 0 are considered bogus
  // each supported object type has an associated ItemType enum value
  // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  // NEVER EVER Change ItemType values as this will break I/O code
  // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  Undefined = 0,
  // some basic types
  Bool = 1, // bool
  Byte = 2, // unsigned char
  SByte = 3, // char
  Short = 4, // short
  UShort = 5, // unsigned short
  Int32 = 6, // int
  UInt32 = 7, // unsigned int
  Int64 = 8, // time_t
  Single = 9, // float
  Double = 10, // double
  Guid = 11,
  String = 12,

  // array of basic .NET data types
  ArrayBool = 13,
  ArrayByte = 14,
  ArraySByte = 15,
  ArrayShort = 16,
  ArrayInt32 = 17,
  ArraySingle = 18,
  ArrayDouble = 19,
  ArrayGuid = 20,
  ArrayString = 21,

  // System::Drawing structs
  Color = 22,
  Point = 23,
  PointF = 24,
  Rectangle = 25,
  RectangleF = 26,
  Size = 27,
  SizeF = 28,
  Font = 29,

  // RMA::OpenNURBS::ValueTypes structs
  Interval = 30,
  Point2d = 31,
  Point3d = 32,
  Point4d = 33,
  Vector2d = 34,
  Vector3d = 35,
  BoundingBox = 36,
  Ray3d = 37,
  PlaneEquation = 38,
  Xform = 39,
  Plane = 40,
  Line = 41,
  Point3f = 42,
  Vector3f = 43,

  // RMA::OpenNURBS classes
  OnBinaryArchiveDictionary = 44,
  OnObject = 45, // don't use this anymore
  OnMeshParameters = 46,
  OnGeometry = 47,
  OnObjRef = 48,
  ArrayObjRef = 49,
  MAXVALUE = 49
};

static bool WriteDictionaryEntryHelper(ON_Write3dmBufferArchive* archive, const ON_wString& key, ItemType it, pybind11::handle& value)
{
  if (ItemType::Undefined == it)
    return false;

  if (!archive->BeginWriteDictionaryEntry((int)it, key))
    return false;
  bool rc = false;
  std::string s;
  switch (it)
  {
  case ItemType::Undefined:
    break;
  case ItemType::Bool:
    {
      bool b = value.cast<bool>();
      rc = archive->WriteBool(b);
    }
    break;
  case ItemType::Byte:
    break;
  case ItemType::SByte:
    break;
  case ItemType::Short:
    break;
  case ItemType::UShort:
    break;
  case ItemType::Int32:
    {
      int i = value.cast<int>();
      rc = archive->WriteInt(i);
    }
    break;
  case ItemType::UInt32:
    break;
  case ItemType::Int64:
    break;
  case ItemType::Single:
    break;
  case ItemType::Double:
    {
      double d = value.cast<double>();
      rc = archive->WriteDouble(d);
    }
    break;
  case ItemType::Guid:
    break;
  case ItemType::String:
    {
      s = pybind11::str(value);
      ON_wString ws(s.c_str());
      rc = archive->WriteString(ws);
    }
    break;
  case ItemType::ArrayBool:
    break;
  case ItemType::ArrayByte:
    break;
  case ItemType::ArraySByte:
    break;
  case ItemType::ArrayShort:
    break;
  case ItemType::ArrayInt32:
    break;
  case ItemType::ArraySingle:
    break;
  case ItemType::ArrayDouble:
    break;
  case ItemType::ArrayGuid:
    break;
  case ItemType::ArrayString:
    break;
  case ItemType::Color:
    break;
  case ItemType::Point:
    break;
  case ItemType::PointF:
    break;
  case ItemType::Rectangle:
    break;
  case ItemType::RectangleF:
    break;
  case ItemType::Size:
    break;
  case ItemType::SizeF:
    break;
  case ItemType::Font:
    break;
  case ItemType::Interval:
    break;
  case ItemType::Point2d:
  {
    ON_2dPoint pt = value.cast<ON_2dPoint>();
    rc = archive->WritePoint(pt);
  }
    break;
  case ItemType::Point3d:
    {
      ON_3dPoint pt = value.cast<ON_3dPoint>();
      rc = archive->WritePoint(pt);
    }
    break;
  case ItemType::Point4d:
    {
      ON_4dPoint pt = value.cast<ON_4dPoint>();
      rc = archive->WritePoint(pt);
    }
    break;
  case ItemType::Vector2d:
    {
      ON_2dVector v = value.cast<ON_2dVector>();
      rc = archive->WriteVector(v);
    }
    break;
  case ItemType::Vector3d:
    {
      ON_3dVector v = value.cast<ON_3dVector>();
      rc = archive->WriteVector(v);
    }
    break;
  case ItemType::BoundingBox:
    break;
  case ItemType::Ray3d:
    break;
  case ItemType::PlaneEquation:
    break;
  case ItemType::Xform:
    break;
  case ItemType::Plane:
    break;
  case ItemType::Line:
    break;
  case ItemType::Point3f:
    break;
  case ItemType::Vector3f:
    break;
  case ItemType::OnBinaryArchiveDictionary:
    break;
  case ItemType::OnObject:
    break;
  case ItemType::OnMeshParameters:
    break;
  case ItemType::OnGeometry:
  {
    BND_GeometryBase* geometry = value.cast<BND_GeometryBase*>();
    rc = archive->WriteObject(*geometry->GeometryPointer());
  }
    break;
  case ItemType::OnObjRef:
    break;
  case ItemType::ArrayObjRef:
    break;
  default:
    break;
  }
  return archive->EndWriteDictionaryEntry() && rc;
}

pybind11::dict BND_ArchivableDictionary::EncodeFromDictionary(pybind11::dict d)
{
  pybind11::dict rc;
  int rhinoversion;
  SetupEncodedDictionaryVersions(rc, rhinoversion);

  ON_Write3dmBufferArchive* archive = ON_WriteBufferArchive_NewMemoryWriter(rhinoversion);
  if (!archive)
    return rc;

  if (!archive->BeginWriteDictionary(RhinoDotNetDictionaryId(), 0, L""))
    return rc;

  for (auto item : d)
  {
    std::string key(pybind11::str(item.first));
    ON_wString wkey(key.c_str());

    ItemType it = ItemType::Undefined;
    if (pybind11::bool_::check_(item.second))
    {
      it = ItemType::Bool; //1
    }
    else if (pybind11::int_::check_(item.second))
    {
      it = ItemType::Int32; //6
    }
    else if (pybind11::float_::check_(item.second))
    {
      it = ItemType::Double; //10
    }
    else if (pybind11::str::check_(item.second))
    {
      it = ItemType::String; //12
    }
    else if (pybind11::isinstance<ON_2dPoint>(item.second))
    {
      it = ItemType::Point2d; //31
    }
    else if (pybind11::isinstance<ON_3dPoint>(item.second))
    {
      it = ItemType::Point3d; //32
    }
    else if (pybind11::isinstance<ON_4dPoint>(item.second))
    {
      it = ItemType::Point4d; //33
    }
    else if (pybind11::isinstance<ON_2dVector>(item.second))
    {
      it = ItemType::Vector2d; //34
    }
    else if (pybind11::isinstance<ON_3dVector>(item.second))
    {
      it = ItemType::Vector3d; //35
    }
    else if (pybind11::isinstance<BND_GeometryBase>(item.second))
    {
      it = ItemType::OnGeometry; //47
    }
    
    if (ItemType::Undefined == it)
    {
      archive->EndWriteDictionary();
      delete archive;
      ON_String msg("Unable to serialize '");
      msg += wkey + "'.";
      msg += "\nAllowed value types are bool, int, float, str, Point2d, Point3d, Point4d,";
      msg += "\nVector2d, Vector3d, and GeometryBase.";
      msg += "\nMore types can be supported; just ask.";
      throw pybind11::cast_error(msg);
    }

    if (ItemType::Undefined != it)
      WriteDictionaryEntryHelper(archive, wkey, it, item.second);
  }
  pybind11::cast_error("");
  archive->EndWriteDictionary();

  std::string data = "";
  int length = (int)archive->SizeOfArchive();
  if (length > 0)
  {
    unsigned char* buffer = (unsigned char*)archive->Buffer();
    data = base64_encode(buffer, length);
  }

  rc["data"] = data;

  delete archive;
  return rc;
}

pybind11::dict BND_ArchivableDictionary::DecodeToDictionary(pybind11::dict jsonObject)
{
  std::string buffer = pybind11::str(jsonObject["data"]);
  std::string decoded = base64_decode(buffer);
  int rhinoversion = jsonObject["archive3dm"].cast<int>();
  int opennurbsversion = jsonObject["opennurbs"].cast<int>();
  int length = static_cast<int>(decoded.length());
  const unsigned char* c = (const unsigned char*)&decoded.at(0);
  // Eliminate potential bogus file versions written
  pybind11::cast_error exception("Unable to decode ArchivableDictionary");
  if (rhinoversion > 5 && rhinoversion < 50)
    throw exception;

  if (length < 1 || nullptr == c)
    throw exception;

  ON_Read3dmBufferArchive archive((size_t)length, c, false, rhinoversion, opennurbsversion);
  ON_UUID dictionaryId;
  unsigned int dictionaryVersion = 0;
  ON_wString dictionaryName;
  if (!archive.BeginReadDictionary(&dictionaryId, &dictionaryVersion, dictionaryName))
    throw exception;
  if (dictionaryId != RhinoDotNetDictionaryId())
    throw exception;

  pybind11::dict rc;
  while (true)
  {
    int i_type = 0;
    ON_wString entryName;
    int read_rc = archive.BeginReadDictionaryEntry(&i_type, entryName);
    if (0 == read_rc)
      throw exception;
    if (1 != read_rc)
      break;
    // Make sure this type is readable with the current version of RhinoCommon.
    // ItemTypes will be expanded with future supported type
    bool readable_type = i_type > 0 && i_type <= (int)(ItemType::MAXVALUE);
    if (readable_type)
    {
      ItemType it = (ItemType)i_type;
      ON_String key = entryName;
      const char* keyname = key.Array();
      switch (it)
      {
      case ItemType::Bool:
        {
          bool b;
          if (archive.ReadBool(&b))
            rc[keyname] = b;
        }
        break;
      case ItemType::Byte:
      case ItemType::SByte:
        {
          char c;
          if (archive.ReadByte(1, &c))
            rc[keyname] = c;
        }
        break;
      case ItemType::Short:
      case ItemType::UShort:
        {
          short s;
          if (archive.ReadShort(&s))
            rc[keyname] = s;
        }
        break;
      case ItemType::Int32:
      case ItemType::UInt32:
        {
          int i;
          if (archive.ReadInt(&i))
            rc[keyname] = i;
        }
        break;
      case ItemType::Int64:
        {
          time_t t;
          if( archive.ReadBigTime(&t) )
            rc[keyname] = (ON__INT64)t;
        }
        break;
      case ItemType::Single:
        {
          float f;
          if (archive.ReadFloat(&f))
            rc[keyname] = f;
        }
        break;
      case ItemType::Double:
        {
          double d;
          if (archive.ReadDouble(&d))
            rc[keyname] = d;
        }
        break;
      case ItemType::Guid:
        {
          ON_UUID id;
          if (archive.ReadUuid(id))
            rc[keyname] = ON_UUID_to_Binding(id);
        }
        break;
      case ItemType::String:
        {
          ON_wString s;
          if (archive.ReadString(s))
            rc[keyname] = std::wstring(s.Array());
        }
        break;
      case ItemType::ArrayBool:
        {
          int count;
          if (archive.ReadInt(&count) && count > 0)
          {
            ON_SimpleArray<bool> bool_array(count);
            char* c = (char*)bool_array.Array();
            if (archive.ReadChar(count, c))
              rc[keyname] = std::vector<bool>(bool_array.Array(), bool_array.Array() + count);
          }
        }
        break;
      case ItemType::ArrayByte:
      case ItemType::ArraySByte:
        {
          int count;
          if (archive.ReadInt(&count) && count > 0)
          {
            ON_SimpleArray<char> char_array(count);
            char* c = char_array.Array();
            if (archive.ReadChar(count, c))
              rc[keyname] = std::vector<char>(char_array.Array(), char_array.Array() + count);
          }
        }
        break;
      case ItemType::ArrayShort:
        {
          int count;
          if (archive.ReadInt(&count) && count > 0)
          {
            ON_SimpleArray<short> short_array(count);
            short* s = short_array.Array();
            if (archive.ReadShort(count, s))
              rc[keyname] = std::vector<short>(short_array.Array(), short_array.Array() + count);
          }
        }
        break;
      case ItemType::ArrayInt32:
        {
          int count;
          if (archive.ReadInt(&count) && count > 0)
          {
            ON_SimpleArray<int> int_array(count);
            int* i = int_array.Array();
            if (archive.ReadInt(count, i))
              rc[keyname] = std::vector<int>(int_array.Array(), int_array.Array() + count);
          }
        }
        break;
      case ItemType::ArraySingle:
        {
          int count;
          if (archive.ReadInt(&count) && count > 0)
          {
            ON_SimpleArray<float> float_array(count);
            float* f = float_array.Array();
            if (archive.ReadFloat(count, f))
              rc[keyname] = std::vector<float>(float_array.Array(), float_array.Array() + count);
          }
        }
        break;
      case ItemType::ArrayDouble:
        {
          int count;
          if (archive.ReadInt(&count) && count > 0)
          {
            ON_SimpleArray<double> double_array(count);
            double* d = double_array.Array();
            if (archive.ReadDouble(count, d))
              rc[keyname] = std::vector<double>(double_array.Array(), double_array.Array() + count);
          }
        }
        break;
      case ItemType::ArrayGuid:
        {
          int count;
          if (archive.ReadInt(&count) && count > 0)
          {
            std::vector<BND_UUID> uuids;
            uuids.reserve(count);
            for (int i = 0; i < count; i++)
            {
              ON_UUID id;
              archive.ReadUuid(id);
              uuids.push_back(ON_UUID_to_Binding(id));
            }
            rc[keyname] = uuids;
          }
        }
        break;
      case ItemType::ArrayString:
        {
          int count;
          if (archive.ReadInt(&count) && count > 0)
          {
            std::vector<std::wstring> strings;
            strings.reserve(count);
            for (int i = 0; i < count; i++)
            {
              ON_wString str;
              if (archive.ReadString(str))
              {
                strings.push_back(std::wstring(str.Array()));
              }
            }
            rc[keyname] = strings;
          }
        }
        break;
      case ItemType::Color:
        {
          ON_Color c;
          if (archive.ReadColor(c))
          {
            rc[keyname] = ON_Color_to_Binding(c);
          }
        }
        break;
      case ItemType::Point:
        {
          int i[2];
          if (archive.ReadInt(2, i))
          {
            rc[keyname] = pybind11::make_tuple(i[0], i[1]);
          }
        }
        break;
      case ItemType::PointF:
        {
          float f[2];
          if (archive.ReadFloat(2, f))
          {
            rc[keyname] = pybind11::make_tuple(f[0], f[1]);
          }
        }
        break;
      case ItemType::Rectangle:
        {
          int i[4];
          if (archive.ReadInt(4, i))
          {
            rc[keyname] = pybind11::make_tuple(i[0], i[1], i[2], i[3]);
          }
        }
        break;
      case ItemType::RectangleF:
        {
          float f[4];
          if (archive.ReadFloat(4, f))
          {
            rc[keyname] = pybind11::make_tuple(f[0], f[1], f[2], f[3]);
          }
        }
        break;
      case ItemType::Size:
        {
          int i[2];
          if (archive.ReadInt(2, i))
          {
            rc[keyname] = pybind11::make_tuple(i[0], i[1]);
          }
        }
        break;
      case ItemType::SizeF:
        {
          float f[2];
          if (archive.ReadFloat(2, f))
          {
            rc[keyname] = pybind11::make_tuple(f[0], f[1]);
          }
        }
        break;
      case ItemType::Font:
        break;
      case ItemType::Interval:
        {
          double d[2];
          if (archive.ReadDouble(2, d))
          {
            rc[keyname] = BND_Interval(ON_Interval(d[0], d[1]));
          }
        }
        break;
      case ItemType::Point2d:
        {
          ON_2dPoint pt;
          if (archive.ReadPoint(pt))
            rc[keyname] = pt;
        }
        break;
      case ItemType::Point3d:
        {
          ON_3dPoint pt;
          if (archive.ReadPoint(pt))
            rc[keyname] = pt;
        }
        break;
      case ItemType::Point4d:
        {
          ON_4dPoint pt;
          if (archive.ReadPoint(pt))
            rc[keyname] = pt;
        }
        break;
      case ItemType::Vector2d:
        {
          ON_2dVector v;
          if (archive.ReadVector(v))
            rc[keyname] = v;
        }
        break;
      case ItemType::Vector3d:
        {
          ON_3dVector v;
          if (archive.ReadVector(v))
            rc[keyname] = v;
        }
        break;
      case ItemType::BoundingBox:
        {
          ON_BoundingBox bb;
          if (archive.ReadBoundingBox(bb))
            rc[keyname] = BND_BoundingBox(bb);
        }
        break;
      case ItemType::Ray3d:
        break;
      case ItemType::PlaneEquation:
        break;
      case ItemType::Xform:
        {
          ON_Xform xf;
          if (archive.ReadXform(xf))
            rc[keyname] = BND_Transform(xf);
        }
        break;
      case ItemType::Plane:
        {
          ON_Plane plane;
          if (archive.ReadPlane(plane))
            rc[keyname] = BND_Plane::FromOnPlane(plane);
        }
        break;
      case ItemType::Line:
        {
          ON_Line line;
          if (archive.ReadLine(line))
            rc[keyname] = line;
        }
        break;
      case ItemType::Point3f:
        {
          ON_3fPoint pt;
          if (archive.ReadFloat(3, &pt.x))
            rc[keyname] = pt;
        }
        break;
      case ItemType::Vector3f:
        {
          ON_3fVector v;
          if (archive.ReadFloat(3, &v.x))
            rc[keyname] = v;
        }
        break;
      case ItemType::OnBinaryArchiveDictionary:
        break;
      case ItemType::OnObject:
        {
          ON_Object* pObject = nullptr;
          if (archive.ReadObject(&pObject))
          {
            rc[keyname] = BND_CommonObject::CreateWrapper(pObject, nullptr);
          }
        }
        break;
      case ItemType::OnMeshParameters:
        {
          ON_MeshParameters mp;
          if (mp.Read(archive))
            rc[keyname] = BND_MeshingParameters(mp);
        }
        break;
      case ItemType::OnGeometry:
        {
          ON_Object* pObject = nullptr;
          if (archive.ReadObject(&pObject))
          {
            rc[keyname] = BND_CommonObject::CreateWrapper(pObject, nullptr);
          }
        }
        break;
      case ItemType::OnObjRef:
        break;
      case ItemType::ArrayObjRef:
        break;
      default:
        break;
      }
    }
    if (!archive.EndReadDictionaryEntry())
      throw exception;
  }

  archive.EndReadDictionary();
  return rc;
}

#endif

RH_C_FUNCTION ON_Object* ON_ReadBufferArchive(int archive_3dm_version, unsigned int archive_on_version, int length, /*ARRAY*/const unsigned char* buffer)
{
  // Eliminate potential bogus file versions written
  if (archive_3dm_version > 5 && archive_3dm_version < 50)
    return nullptr;
  ON_Object* rc = nullptr;
  if( length>0 && buffer )
  {
    ON_Read3dmBufferArchive archive(length, buffer, false, archive_3dm_version, archive_on_version);
    archive.ReadObject( &rc );
  }
  return rc;
}

#if defined(__EMSCRIPTEN__)
BND_CommonObject* BND_CommonObject::Decode(emscripten::val jsonObject)
{
  std::string buffer = jsonObject["data"].as<std::string>();
  std::string decoded = base64_decode(buffer);
  int rhinoversion = jsonObject["archive3dm"].as<int>();
  int opennurbsversion = jsonObject["opennurbs"].as<int>();
  int length = decoded.length();
  const unsigned char* c = (const unsigned char*)&decoded.at(0);
  ON_Object* obj = ON_ReadBufferArchive(rhinoversion, opennurbsversion, length, c);
  return CreateWrapper(obj, nullptr);
}
#endif


#if defined(ON_PYTHON_COMPILE)

BND_CommonObject* BND_CommonObject::Decode(pybind11::dict jsonObject)
{
  std::string buffer = pybind11::str(jsonObject["data"]);
  std::string decoded = base64_decode(buffer);
  int rhinoversion = jsonObject["archive3dm"].cast<int>();
  int opennurbsversion = jsonObject["opennurbs"].cast<int>();
  int length = static_cast<int>(decoded.length());
  const unsigned char* c = (const unsigned char*)&decoded.at(0);
  ON_Object* obj = ON_ReadBufferArchive(rhinoversion, opennurbsversion, length, c);
  return CreateWrapper(obj, nullptr);
}
#endif


bool BND_CommonObject::SetUserString(std::wstring key, std::wstring value)
{
  return m_object->SetUserString(key.c_str(), value.c_str());
}

std::wstring BND_CommonObject::GetUserString(std::wstring key)
{
  ON_wString value;
  if (m_object->GetUserString(key.c_str(), value))
  {
    return std::wstring(value);
  }
  return std::wstring(L"");
}

#if defined(ON_PYTHON_COMPILE)
pybind11::tuple BND_CommonObject::GetUserStrings() const
{
  ON_ClassArray<ON_wString> keys;
  m_object->GetUserStringKeys(keys);
  pybind11::tuple rc(keys.Count());
  for (int i = 0; i < keys.Count(); i++)
  {
    ON_wString sval;
    m_object->GetUserString(keys[i].Array(), sval);
    pybind11::tuple keyval(2);
    keyval[0] = std::wstring(keys[i].Array());
    keyval[1] = std::wstring(sval.Array());
    rc[i] = keyval;
  }
  return rc;
}

std::wstring BND_CommonObject::RdkXml() const
{
  std::wstring rc;
  ON_wString xmlstring;
  if (ONX_Model::GetRDKObjectInformation(*m_object, xmlstring))
  {
    rc = xmlstring.Array();
    return rc;
  }
  return rc;
}

#endif




#if defined(ON_PYTHON_COMPILE)
namespace py = pybind11;
void initObjectBindings(pybind11::module& m)
{
  py::class_<BND_CommonObject>(m, "CommonObject")
    .def("Encode", &BND_CommonObject::Encode)
    .def_static("Decode", &BND_CommonObject::Decode)
    .def("SetUserString", &BND_CommonObject::SetUserString)
    .def("GetUserString", &BND_CommonObject::GetUserString)
    .def_property_readonly("UserStringCount", &BND_CommonObject::UserStringCount)
    .def("GetUserStrings", &BND_CommonObject::GetUserStrings)
    .def("RdkXml", &BND_CommonObject::RdkXml)
    ;

  py::class_<BND_ArchivableDictionary>(m, "ArchivableDictionary")
    .def_static("EncodeDict", &BND_ArchivableDictionary::EncodeFromDictionary)
    .def_static("DecodeDict", &BND_ArchivableDictionary::DecodeToDictionary)
    ;
}
#endif

#if defined(ON_WASM_COMPILE)
using namespace emscripten;

void initObjectBindings(void*)
{
  class_<BND_CommonObject>("CommonObject")
    .function("encode", &BND_CommonObject::Encode)
    .function("toJSON", &BND_CommonObject::toJSON)
    .class_function("decode", &BND_CommonObject::Decode, allow_raw_pointers())
    .function("setUserString", &BND_CommonObject::SetUserString)
    .function("getUserString", &BND_CommonObject::GetUserString)
    .property("userStringCount", &BND_CommonObject::UserStringCount)
    ;
}
#endif
